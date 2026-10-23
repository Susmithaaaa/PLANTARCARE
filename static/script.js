
document.addEventListener("DOMContentLoaded", function () {

    // ==================================================
    // SIDEBAR - OPEN / CLOSE
    // ==================================================

    const sidebar = document.querySelector(".sidebar");
    const overlay = document.querySelector(".sidebar-overlay");
    const menuButton = document.querySelector("[data-menu]");

    function openSidebar() {
        document.body.classList.add("menu-open");

        if (menuButton) {
            menuButton.setAttribute("aria-expanded", "true");
        }
    }

    function closeSidebar() {
        document.body.classList.remove("menu-open");

        if (menuButton) {
            menuButton.setAttribute("aria-expanded", "false");
        }
    }

    if (sidebar && overlay && menuButton) {

        menuButton.setAttribute("aria-expanded", "false");

        menuButton.addEventListener("click", function () {
            if (document.body.classList.contains("menu-open")) {
                closeSidebar();
            } else {
                openSidebar();
            }
        });

        overlay.addEventListener("click", closeSidebar);

        document.addEventListener("keydown", function (event) {
            if (event.key === "Escape") {
                closeSidebar();
            }
        });

        sidebar.querySelectorAll(".nav-link, .account-link")
            .forEach(function (link) {
                link.addEventListener("click", closeSidebar);
            });
    }


    // ==================================================
    // LIVE BMI CALCULATOR
    // ==================================================

    const heightInput = document.querySelector("#height");
    const weightInput = document.querySelector("#weight");
    const bmiPreview = document.querySelector("#bmiPreview");

    const bmiCategoryPreview =
        document.querySelector("#bmiCategoryPreview");

    function calculateBMI() {

        if (!heightInput || !weightInput || !bmiPreview) {
            return;
        }

        const height = parseFloat(heightInput.value);
        const weight = parseFloat(weightInput.value);

        if (!height || !weight || height <= 0 || weight <= 0) {

            bmiPreview.textContent = "--";

            if (bmiCategoryPreview) {
                bmiCategoryPreview.textContent =
                    "Enter height and weight";
            }

            return;
        }

        const bmi = weight / Math.pow(height / 100, 2);

        bmiPreview.textContent = bmi.toFixed(1);

        if (bmiCategoryPreview) {

            if (bmi < 18.5) {
                bmiCategoryPreview.textContent = "Underweight";

            } else if (bmi < 25) {
                bmiCategoryPreview.textContent = "Healthy Range";

            } else if (bmi < 30) {
                bmiCategoryPreview.textContent = "Overweight";

            } else {
                bmiCategoryPreview.textContent = "Higher BMI Range";
            }
        }
    }

    if (heightInput) {
        heightInput.addEventListener("input", calculateBMI);
    }

    if (weightInput) {
        weightInput.addEventListener("input", calculateBMI);
    }

    calculateBMI();


    // ==================================================
    // CARE STEPPER
    // ==================================================

    const careSteps = document.querySelectorAll("[data-care-step]");
    const stepDots = document.querySelectorAll("[data-step-dot]");

    function showCareStep(stepNumber) {

        careSteps.forEach(function (step, index) {
            step.classList.toggle("active", index === stepNumber);
        });

        stepDots.forEach(function (dot, index) {
            dot.classList.toggle("active", index <= stepNumber);
        });

        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
    }

    document.querySelectorAll("[data-next-care]")
        .forEach(function (button) {

            button.addEventListener("click", function () {

                const nextStep = parseInt(
                    button.dataset.nextCare,
                    10
                );

                if (
                    !Number.isNaN(nextStep) &&
                    nextStep >= 0 &&
                    nextStep < careSteps.length
                ) {
                    showCareStep(nextStep);
                }
            });
        });

    document.querySelectorAll("[data-back-care]")
        .forEach(function (button) {

            button.addEventListener("click", function () {

                const previousStep = parseInt(
                    button.dataset.backCare,
                    10
                );

                if (
                    !Number.isNaN(previousStep) &&
                    previousStep >= 0 &&
                    previousStep < careSteps.length
                ) {
                    showCareStep(previousStep);
                }
            });
        });

    if (careSteps.length > 0) {
        showCareStep(0);
    }


    // ==================================================
    // CAMERA ELEMENTS
    // ==================================================

    const startCameraButton =
        document.querySelector("#startCamera");

    const stopCameraButton =
        document.querySelector("#stopCamera");

    const cameraVideo =
        document.querySelector("#cameraVideo");

    const cameraPlaceholder =
        document.querySelector("#cameraPlaceholder");

    const cameraStatus =
        document.querySelector("#cameraStatus");

    const startCameraGame =
        document.querySelector("#startCameraGame");

    const resetCameraGame =
        document.querySelector("#resetCameraGame");

    const gameArea =
        document.querySelector("#cameraGameArea");

    const cameraTarget =
        document.querySelector("#cameraTarget");

    const cameraScoreElement =
        document.querySelector("#cameraScore");

    const cameraTimeElement =
        document.querySelector("#cameraTime");

    const cameraHitsElement =
        document.querySelector("#cameraHits");

    const cameraGameMessage =
        document.querySelector("#cameraGameMessage");

    let cameraStream = null;
    let cameraStarting = false;

    let score = 0;
    let hits = 0;
    let timeLeft = 30;

    let gameRunning = false;
    let gameTimer = null;


    // ==================================================
    // CAMERA GAME UI
    // ==================================================

    function updateCameraGameUI() {

        if (cameraScoreElement) {
            cameraScoreElement.textContent = score;
        }

        if (cameraHitsElement) {
            cameraHitsElement.textContent = hits;
        }

        if (cameraTimeElement) {
            cameraTimeElement.textContent = timeLeft;
        }
    }


    // ==================================================
    // STOP CAMERA GAME TIMER
    // ==================================================

    function stopCameraGameTimer() {

        gameRunning = false;

        if (gameTimer !== null) {
            clearInterval(gameTimer);
            gameTimer = null;
        }
    }


    // ==================================================
    // MOVE GAME TARGET
    // ==================================================

    function moveTarget() {

        if (!gameArea || !cameraTarget) {
            return;
        }

        const areaWidth = gameArea.clientWidth;
        const areaHeight = gameArea.clientHeight;

        const targetWidth = cameraTarget.offsetWidth || 62;
        const targetHeight = cameraTarget.offsetHeight || 62;

        const maxX = Math.max(0, areaWidth - targetWidth);
        const maxY = Math.max(0, areaHeight - targetHeight);

        const x = Math.random() * maxX;
        const y = Math.random() * maxY;

        cameraTarget.style.left = x + "px";
        cameraTarget.style.top = y + "px";
    }


    // ==================================================
    // START CAMERA
    // ==================================================

    async function startWebcam() {

        if (cameraStarting) {
            return false;
        }

        if (!cameraVideo) {

            if (cameraStatus) {
                cameraStatus.textContent =
                    "Camera video element was not found.";
            }

            return false;
        }

        if (
            !navigator.mediaDevices ||
            !navigator.mediaDevices.getUserMedia
        ) {

            if (cameraStatus) {
                cameraStatus.textContent =
                    "Camera unavailable. Open the app using localhost or HTTPS.";
            }

            return false;
        }

        if (cameraStream && cameraStream.active) {

            if (
                cameraVideo.srcObject === cameraStream &&
                cameraVideo.videoWidth > 0 &&
                !cameraVideo.paused
            ) {
                return true;
            }

            // Release an old or inactive stream.
            cameraStream.getTracks().forEach(function (track) {
                track.stop();
            });

            cameraStream = null;
        }

        cameraStarting = true;

        if (startCameraButton) {
            startCameraButton.disabled = true;
        }

        if (cameraStatus) {
            cameraStatus.textContent = "Starting camera...";
        }

        try {

            cameraVideo.pause();
            cameraVideo.srcObject = null;

            cameraStream =
                await navigator.mediaDevices.getUserMedia({

                    video: {
                        facingMode: "user",
                        width: { ideal: 640 },
                        height: { ideal: 480 }
                    },

                    audio: false
                });

            cameraVideo.srcObject = cameraStream;
            cameraVideo.muted = true;
            cameraVideo.autoplay = true;
            cameraVideo.playsInline = true;

            cameraVideo.style.display = "block";
            cameraVideo.style.visibility = "visible";
            cameraVideo.style.width = "100%";
            cameraVideo.style.height = "280px";
            cameraVideo.style.objectFit = "cover";

            if (cameraPlaceholder) {
                cameraPlaceholder.style.display = "none";
            }

            // Wait for the camera to produce video frames.
            await new Promise(function (resolve, reject) {

                let finished = false;

                let timeoutId;

                function cleanup() {

                    clearTimeout(timeoutId);

                    cameraVideo.removeEventListener(
                        "loadeddata",
                        onLoaded
                    );

                    cameraVideo.removeEventListener(
                        "error",
                        onError
                    );
                }

                function onLoaded() {

                    if (finished) return;

                    finished = true;
                    cleanup();
                    resolve();
                }

                function onError() {

                    if (finished) return;

                    finished = true;
                    cleanup();

                    reject(
                        new Error("The camera video could not load.")
                    );
                }

                timeoutId = setTimeout(function () {

                    if (finished) return;

                    finished = true;
                    cleanup();

                    reject(
                        new Error(
                            "Camera opened, but no video frames arrived."
                        )
                    );

                }, 10000);

                cameraVideo.addEventListener(
                    "loadeddata",
                    onLoaded
                );

                cameraVideo.addEventListener(
                    "error",
                    onError
                );

                if (
                    cameraVideo.readyState >= 2 &&
                    cameraVideo.videoWidth > 0
                ) {
                    onLoaded();
                }
            });

            await cameraVideo.play();

            if (cameraStatus) {
                cameraStatus.textContent =
                    "Camera is on. Live preview is ready.";
            }

            if (cameraGameMessage) {
                cameraGameMessage.textContent =
                    "Camera ready. Press Start Game.";
            }

            return true;

        } catch (error) {

            console.error("Camera error:", error);

            if (cameraStream) {

                cameraStream.getTracks().forEach(function (track) {
                    track.stop();
                });

                cameraStream = null;
            }

            cameraVideo.pause();
            cameraVideo.srcObject = null;
            cameraVideo.style.display = "none";

            if (cameraPlaceholder) {
                cameraPlaceholder.style.display = "flex";
            }

            if (cameraStatus) {

                if (
                    error.name === "NotAllowedError" ||
                    error.name === "SecurityError"
                ) {

                    cameraStatus.textContent =
                        "Camera permission denied. Allow camera access in Chrome settings.";

                } else if (error.name === "NotFoundError") {

                    cameraStatus.textContent =
                        "No camera device found. Check your laptop camera.";

                } else if (error.name === "NotReadableError") {

                    cameraStatus.textContent =
                        "Camera is busy. Close other apps using the camera.";

                } else {

                    cameraStatus.textContent =
                        "Camera error: " + error.message;
                }
            }

            return false;

        } finally {

            cameraStarting = false;

            if (startCameraButton) {
                startCameraButton.disabled = false;
            }
        }
    }


    // ==================================================
    // FINISH CAMERA GAME
    // ==================================================

    function finishCameraGame() {

        stopCameraGameTimer();

        if (cameraTarget) {
            cameraTarget.style.display = "none";
        }

        if (cameraGameMessage) {
            cameraGameMessage.textContent =
                "Game completed! Final score: " +
                score + " points.";
        }
    }


    // ==================================================
    // STOP CAMERA
    // ==================================================

    function stopWebcam() {

        stopCameraGameTimer();

        if (cameraStream) {

            cameraStream.getTracks().forEach(function (track) {
                track.stop();
            });

            cameraStream = null;
        }

        if (cameraVideo) {

            cameraVideo.pause();
            cameraVideo.srcObject = null;
            cameraVideo.style.display = "none";
        }

        if (cameraPlaceholder) {
            cameraPlaceholder.style.display = "flex";
        }

        if (cameraStatus) {
            cameraStatus.textContent = "Camera is off.";
        }

        if (cameraTarget) {
            cameraTarget.style.display = "none";
        }

        if (cameraGameMessage) {
            cameraGameMessage.textContent =
                "Start Camera first, then press Start Game.";
        }
    }

    if (startCameraButton) {

        startCameraButton.addEventListener("click", function () {
            startWebcam();
        });
    }

    if (stopCameraButton) {

        stopCameraButton.addEventListener("click", function () {
            stopWebcam();
        });
    }


    // ==================================================
    // START CAMERA TARGET GAME
    // ==================================================

    async function startTargetGame() {

        if (gameRunning) {
            return;
        }

        if (
            !cameraStream ||
            !cameraStream.active ||
            !cameraVideo ||
            cameraVideo.paused ||
            cameraVideo.videoWidth === 0
        ) {

            const cameraGranted = await startWebcam();

            if (!cameraGranted) {

                if (cameraGameMessage) {
                    cameraGameMessage.textContent =
                        "Please start the camera before playing.";
                }

                return;
            }
        }

        stopCameraGameTimer();

        score = 0;
        hits = 0;
        timeLeft = 30;

        gameRunning = true;

        updateCameraGameUI();

        if (cameraTarget) {
            cameraTarget.style.display = "flex";
        }

        if (cameraGameMessage) {
            cameraGameMessage.textContent =
                "Game started! Hit the target.";
        }

        moveTarget();

        gameTimer = setInterval(function () {

            timeLeft--;

            updateCameraGameUI();

            if (timeLeft <= 0) {
                finishCameraGame();
            }

        }, 1000);
    }

    if (startCameraGame) {

        startCameraGame.addEventListener("click", function () {
            startTargetGame();
        });
    }


    // ==================================================
    // CAMERA TARGET CLICK
    // ==================================================

    if (cameraTarget) {

        cameraTarget.addEventListener("click", function () {

            if (!gameRunning) {
                return;
            }

            hits++;
            score += 10;

            updateCameraGameUI();
            moveTarget();

            if (cameraGameMessage) {
                cameraGameMessage.textContent =
                    "Target hit! +10 points.";
            }
        });
    }


    // ==================================================
    // RESET CAMERA GAME
    // ==================================================

    if (resetCameraGame) {

        resetCameraGame.addEventListener("click", function () {

            stopCameraGameTimer();

            score = 0;
            hits = 0;
            timeLeft = 30;

            updateCameraGameUI();

            if (cameraTarget) {
                cameraTarget.style.display = "none";
            }

            if (cameraGameMessage) {

                cameraGameMessage.textContent =
                    cameraStream && cameraStream.active
                        ? "Camera ready. Press Start Game."
                        : "Start Camera first, then press Start Game.";
            }
        });
    }

    updateCameraGameUI();


    // ==================================================
    // CAMERA-FREE TOE TAP GAME
    // ==================================================

    const tapButton = document.querySelector("#tapButton");

    const gameScoreElement =
        document.querySelector("#gameScore");

    const gameMessage =
        document.querySelector("#gameMessage");

    let tapScore = 0;

    if (tapButton) {

        tapButton.addEventListener("click", function () {

            tapScore++;

            if (gameScoreElement) {
                gameScoreElement.textContent = tapScore;
            }

            if (gameMessage) {

                if (tapScore >= 10) {

                    gameMessage.textContent =
                        "Great job! Challenge completed.";

                } else {

                    gameMessage.textContent =
                        "Good! Keep the movement comfortable.";
                }
            }
        });
    }


    // ==================================================
    // CLEANUP WHEN LEAVING PAGE
    // ==================================================

    window.addEventListener("pagehide", function () {

        stopCameraGameTimer();

        if (cameraStream) {

            cameraStream.getTracks().forEach(function (track) {
                track.stop();
            });

            cameraStream = null;
        }
    });

});
