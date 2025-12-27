pipeline {
    agent {
        label 'MyLaptopPool'   // Windows Jenkins agent label
    }

    environment {
        SHIVA_TOKEN  = credentials('ShivaToken')     // GitHub PAT
        TRIAGE_TOKEN = credentials('TriageToken')    // GitHub PAT
    }

    stages {

        stage('🧩 Setup Python & Playwright') {
            steps {
                powershell '''
                Write-Host "🔧 Setting up Python & Playwright..."

                py -3.12 -m pip install --upgrade pip
                py -3.12 -m pip install pytest playwright
                py -3.12 -m playwright install

                Write-Host "✅ Python & Playwright ready."
                '''
            }
        }

        stage('📥 Fetch Code') {
            steps {
                powershell '''
                Write-Host "📥 Cloning Test Repository..."

                if (Test-Path "TeamTests") {
                    Remove-Item -Recurse -Force "TeamTests"
                }

                git clone https://$env:SHIVA_TOKEN@github.com/sivaparvathi-coastal7/login_signup.git TeamTests

                if ($LASTEXITCODE -ne 0) {
                    Write-Error "❌ Clone failed. Check ShivaToken."
                    exit 1
                }

                Write-Host "✅ Repository cloned."
                '''
            }
        }

        stage('▶️ Run Playwright Tests') {
            steps {
                powershell '''
                Write-Host "🚀 Creating guaranteed failure test..."

                $test = @(
                    "from playwright.sync_api import sync_playwright",
                    "",
                    "def test_google_title():",
                    "    with sync_playwright() as p:",
                    "        browser = p.chromium.launch(headless=True)",
                    "        page = browser.new_page()",
                    "        page.goto('https://google.com')",
                    "        title = page.title()",
                    "        print(f'Title is: {title}')",
                    "        browser.close()",
                    "        assert 'Yahoo' in title"
                )

                $test | Out-File -FilePath "TeamTests/test_guaranteed.py" -Encoding UTF8

                cd TeamTests
                Write-Host "🧪 Running pytest..."

                cmd /c "py -3.12 -m pytest -vv test_guaranteed.py > error_log.txt 2>&1"

                $exitCode = $LASTEXITCODE
                Get-Content error_log.txt

                if ($exitCode -ne 0) {
                    Write-Error "❌ Tests failed."
                    exit 1
                }

                Write-Host "✅ Tests passed."
                '''
            }
        }
    }

    post {
        failure {
            powershell '''
            Write-Host "🚨 Pipeline failed — starting triage..."

            if (Test-Path "TeamTests/error_log.txt") {
                $ErrorContent = Get-Content "TeamTests/error_log.txt" |
                                Select-Object -Last 50 | Out-String
            } else {
                $ErrorContent = "No error log found."
            }

            $JsonData = @{
                test_name             = "Login Signup Tests (Windows Native)"
                file_path             = "TeamTests/test_guaranteed.py"
                error_message          = "Playwright test failure"
                stack_trace            = $ErrorContent
                logs                   = $ErrorContent
                llm_model              = "gemma:2b"
                bert_url               = "http://127.0.0.1:8001"
                labels                 = @("bug","auto-report","windows")
                test_url               = "https://github.com/sivaparvathi-coastal7/login_signup"
                playwright_script_url  = "https://github.com/sivaparvathi-coastal7/login_signup/blob/main/test_guaranteed.py"
            }

            $ApiUrl = "https://krystin-unoutspoken-terica.ngrok-free.dev/report-failure"

            try {
                Invoke-RestMethod -Uri $ApiUrl -Method POST `
                    -Body ($JsonData | ConvertTo-Json -Depth 4) `
                    -ContentType "application/json"
                Write-Host "✅ API updated."
            } catch {
                Write-Host "⚠️ API not reachable."
            }

            if (Test-Path "TriageRepo") {
                Remove-Item -Recurse -Force "TriageRepo"
            }

            git clone https://$env:TRIAGE_TOKEN@github.com/Aswini-Kamireddy/triage_engine.git TriageRepo
            cd TriageRepo

            $ReportName = "failure_report_${env:BUILD_ID}.json"
            $JsonData | ConvertTo-Json -Depth 4 | Out-File $ReportName -Encoding UTF8

            git config user.email "bot@qagarden.com"
            git config user.name "Windows Bot"

            git add .
            git commit -m "Failure Report - Build ${env:BUILD_ID}"
            git push origin main

            Write-Host "✅ Failure report pushed."
            '''
        }
    }
}
