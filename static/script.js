document.addEventListener(
    "DOMContentLoaded",
    function () {


        // ==================================================
        // SIDEBAR
        // ==================================================

        const sidebar =
            document.querySelector(
                ".sidebar"
            );


        const overlay =
            document.querySelector(
                ".sidebar-overlay"
            );


        const menuButton =
            document.querySelector(
                "[data-menu]"
            );


        if (
            menuButton &&
            sidebar &&
            overlay
        ) {

            menuButton.addEventListener(
                "click",
                function () {

                    sidebar.classList.toggle(
                        "open"
                    );

                    overlay.classList.toggle(
                        "show"
                    );

                }
            );

        }


        if (overlay) {

            overlay.addEventListener(
                "click",
                function () {

                    if (sidebar) {

                        sidebar.classList.remove(
                            "open"
                        );

                    }

                    overlay.classList.remove(
                        "show"
                    );

                }
            );

        }



        // ==================================================
        // LIVE BMI CALCULATOR
        // ==================================================

        const heightInput =
            document.querySelector(
                "#height"
            );


        const weightInput =
            document.querySelector(
                "#weight"
            );


        const bmiPreview =
            document.querySelector(
                "#bmiPreview"
            );


        const bmiCategoryPreview =
            document.querySelector(
                "#bmiCategoryPreview"
            );


        function calculateBMI() {

            if (
                !heightInput ||
                !weightInput ||
                !bmiPreview
            ) {

                return;

            }


            const height =
                parseFloat(
                    heightInput.value
                );


            const weight =
                parseFloat(
                    weightInput.value
                );


            if (
                !height ||
                !weight ||
                height <= 0 ||
                weight <= 0
            ) {

                bmiPreview.textContent =
                    "--";


                if (
                    bmiCategoryPreview
                ) {

                    bmiCategoryPreview.textContent =
                        "Enter height and weight";

                }

                return;

            }


            const bmi =
                weight /
                Math.pow(
                    height / 100,
                    2
                );


            bmiPreview.textContent =
                bmi.toFixed(1);


            if (
                bmiCategoryPreview
            ) {

                if (
                    bmi < 18.5
                ) {

                    bmiCategoryPreview.textContent =
                        "Underweight";

                }

                else if (
                    bmi < 25
                ) {

                    bmiCategoryPreview.textContent =
                        "Healthy Range";

                }

                else if (
                    bmi < 30
                ) {

                    bmiCategoryPreview.textContent =
                        "Overweight";

                }

                else {

                    bmiCategoryPreview.textContent =
                        "Higher BMI Range";

                }

            }

        }


        if (heightInput) {

            heightInput.addEventListener(
                "input",
                calculateBMI
            );

        }


        if (weightInput) {

            weightInput.addEventListener(
                "input",
                calculateBMI
            );

        }


        calculateBMI();



        // ==================================================
        // CARE STEPPER
        // ==================================================

        const careSteps =
            document.querySelectorAll(
                "[data-care-step]"
            );


        const stepDots =
            document.querySelectorAll(
                "[data-step-dot]"
            );


        function showCareStep(
            stepNumber
        ) {

            careSteps.forEach(
                function (
                    step,
                    index
                ) {

                    step.classList.toggle(
                        "active",
                        index === stepNumber
                    );

                }
            );


            stepDots.forEach(
                function (
                    dot,
                    index
                ) {

                    dot.classList.toggle(
                        "active",
                        index <= stepNumber
                    );

                }
            );


            window.scrollTo({

                top: 0,

                behavior: "smooth"

            });

        }


        document
            .querySelectorAll(
                "[data-next-care]"
            )
            .forEach(
                function (button) {

                    button.addEventListener(
                        "click",
                        function () {

                            const nextStep =
                                parseInt(
                                    button.dataset.nextCare
                                );


                            showCareStep(
                                nextStep
                            );

                        }
                    );

                }
            );


        document
            .querySelectorAll(
                "[data-back-care]"
            )
            .forEach(
                function (button) {

                    button.addEventListener(
                        "click",
                        function () {

                            const previousStep =
                                parseInt(
                                    button.dataset.backCare
                                );


                            showCareStep(
                                previousStep
                            );

                        }
                    );

                }
            );


        if (
            careSteps.length > 0
        ) {

            showCareStep(0);

        }



        // ==================================================
        // CAMERA ELEMENTS
        // ==================================================

        const startCamera =
            document.querySelector(
                "#startCamera"
            );


        const stopCamera =
            document.querySelector(
                "#stopCamera"
            );


        const cameraVideo =
            document.querySelector(
                "#cameraVideo"
            );


        const cameraPlaceholder =
            document.querySelector(
                "#cameraPlaceholder"
            );


        const cameraStatus =
            document.querySelector(
                "#cameraStatus"
            );


        let cameraStream = null;



        // ==================================================
        // START CAMERA
        // ==================================================

        async function startWebcam() {

            if (
                !navigator.mediaDevices ||
                !navigator.mediaDevices.getUserMedia
            ) {

                if (cameraStatus) {

                    cameraStatus.textContent =
                        "Camera API is not available in this browser.";

                }

                return false;

            }


            try {

                cameraStream =
                    await navigator.mediaDevices
                        .getUserMedia({

                            video: {

                                facingMode:
                                    "user",

                                width: {

                                    ideal: 1280

                                },

                                height: {

                                    ideal: 720

                                }

                            },

                            audio: false

                        });


                if (cameraVideo) {

                    cameraVideo.srcObject =
                        cameraStream;

                }


                if (
                    cameraPlaceholder
                ) {

                    cameraPlaceholder.style.display =
                        "none";

                }


                if (
                    cameraStatus
                ) {

                    cameraStatus.textContent =
                        "Camera access granted.";

                }


                return true;

            }


            catch (error) {

                console.error(
                    "Camera error:",
                    error
                );


                if (
                    cameraStatus
                ) {

                    cameraStatus.textContent =
                        "Camera permission was not granted. Please allow camera access in Chrome.";

                }


                return false;

            }

        }



        // ==================================================
        // STOP CAMERA
        // ==================================================

        function stopWebcam() {

            if (cameraStream) {

                cameraStream
                    .getTracks()
                    .forEach(
                        function (track) {

                            track.stop();

                        }
                    );

            }


            cameraStream = null;


            if (cameraVideo) {

                cameraVideo.srcObject =
                    null;

            }


            if (
                cameraPlaceholder
            ) {

                cameraPlaceholder.style.display =
                    "flex";

            }


            if (
                cameraStatus
            ) {

                cameraStatus.textContent =
                    "Camera is off.";

            }

        }



        if (startCamera) {

            startCamera.addEventListener(
                "click",
                async function () {

                    await startWebcam();

                }
            );

        }



        if (stopCamera) {

            stopCamera.addEventListener(
                "click",
                function () {

                    stopWebcam();

                }
            );

        }



        // ==================================================
        // CAMERA TARGET GAME
        // ==================================================

        const startCameraGame =
            document.querySelector(
                "#startCameraGame"
            );


        const resetCameraGame =
            document.querySelector(
                "#resetCameraGame"
            );


        const gameArea =
            document.querySelector(
                "#cameraGameArea"
            );


        const cameraTarget =
            document.querySelector(
                "#cameraTarget"
            );


        const cameraScore =
            document.querySelector(
                "#cameraScore"
            );


        const cameraTime =
            document.querySelector(
                "#cameraTime"
            );


        const cameraHits =
            document.querySelector(
                "#cameraHits"
            );


        const cameraGameMessage =
            document.querySelector(
                "#cameraGameMessage"
            );


        let score = 0;

        let hits = 0;

        let timeLeft = 30;

        let gameRunning = false;

        let gameTimer = null;



        // ==================================================
        // UPDATE CAMERA GAME UI
        // ==================================================

        function updateCameraGameUI() {

            if (cameraScore) {

                cameraScore.textContent =
                    score;

            }


            if (cameraHits) {

                cameraHits.textContent =
                    hits;

            }


            if (cameraTime) {

                cameraTime.textContent =
                    timeLeft;

            }

        }



        // ==================================================
        // MOVE TARGET
        // ==================================================

        function moveTarget() {

            if (
                !gameArea ||
                !cameraTarget
            ) {

                return;

            }


            const areaWidth =
                gameArea.clientWidth;


            const areaHeight =
                gameArea.clientHeight;


            const targetWidth =
                cameraTarget.offsetWidth;


            const targetHeight =
                cameraTarget.offsetHeight;


            const maxX =
                Math.max(
                    areaWidth -
                    targetWidth -
                    10,
                    10
                );


            const maxY =
                Math.max(
                    areaHeight -
                    targetHeight -
                    10,
                    10
                );


            const x =
                Math.random() *
                maxX;


            const y =
                Math.random() *
                maxY;


            cameraTarget.style.left =
                x + "px";


            cameraTarget.style.top =
                y + "px";

        }



        // ==================================================
        // FINISH GAME
        // ==================================================

        function finishCameraGame() {

            gameRunning = false;


            if (gameTimer) {

                clearInterval(
                    gameTimer
                );

                gameTimer = null;

            }


            if (cameraTarget) {

                cameraTarget.style.display =
                    "none";

            }


            if (
                cameraGameMessage
            ) {

                cameraGameMessage.textContent =
                    "Game completed! Final score: " +
                    score +
                    " points.";

            }

        }



        // ==================================================
        // START CAMERA GAME
        // ==================================================

        async function startTargetGame() {

            if (!cameraStream) {

                const cameraGranted =
                    await startWebcam();


                if (!cameraGranted) {

                    if (
                        cameraGameMessage
                    ) {

                        cameraGameMessage.textContent =
                            "Please allow camera access before starting the game.";

                    }

                    return;

                }

            }


            score = 0;

            hits = 0;

            timeLeft = 30;

            gameRunning = true;


            updateCameraGameUI();


            if (cameraTarget) {

                cameraTarget.style.display =
                    "flex";

            }


            if (
                cameraGameMessage
            ) {

                cameraGameMessage.textContent =
                    "Game started! Hit the target!";

            }


            moveTarget();


            if (gameTimer) {

                clearInterval(
                    gameTimer
                );

            }


            gameTimer =
                setInterval(
                    function () {

                        timeLeft--;


                        updateCameraGameUI();


                        if (
                            timeLeft <= 0
                        ) {

                            finishCameraGame();

                        }

                    },
                    1000
                );

        }



        // ==================================================
        // TARGET CLICK
        // ==================================================

        if (cameraTarget) {

            cameraTarget.addEventListener(
                "click",
                function () {

                    if (!gameRunning) {

                        return;

                    }


                    hits++;

                    score += 10;


                    updateCameraGameUI();


                    moveTarget();


                    if (
                        cameraGameMessage
                    ) {

                        cameraGameMessage.textContent =
                            "Target hit! +10 points";

                    }

                }
            );

        }



        // ==================================================
        // START GAME BUTTON
        // ==================================================

        if (startCameraGame) {

            startCameraGame.addEventListener(
                "click",
                function () {

                    startTargetGame();

                }
            );

        }



        // ==================================================
        // RESET GAME
        // ==================================================

        if (resetCameraGame) {

            resetCameraGame.addEventListener(
                "click",
                function () {

                    if (gameTimer) {

                        clearInterval(
                            gameTimer
                        );

                        gameTimer = null;

                    }


                    gameRunning = false;


                    score = 0;

                    hits = 0;

                    timeLeft = 30;


                    updateCameraGameUI();


                    if (cameraTarget) {

                        cameraTarget.style.display =
                            "none";

                    }


                    if (
                        cameraGameMessage
                    ) {

                        cameraGameMessage.textContent =
                            "Start Camera first, then press Start Game.";

                    }

                }
            );

        }



        // ==================================================
        // CAMERA-FREE TOE TAP GAME
        // ==================================================

        const tapButton =
            document.querySelector(
                "#tapButton"
            );


        const gameScore =
            document.querySelector(
                "#gameScore"
            );


        const gameMessage =
            document.querySelector(
                "#gameMessage"
            );


        let tapScore = 0;


        if (tapButton) {

            tapButton.addEventListener(
                "click",
                function () {

                    tapScore++;


                    if (gameScore) {

                        gameScore.textContent =
                            tapScore;

                    }


                    if (gameMessage) {

                        gameMessage.textContent =
                            "Good! Keep the movement comfortable.";

                    }

                }
            );

        }



        // ==================================================
        // CLEANUP CAMERA WHEN LEAVING PAGE
        // ==================================================

        window.addEventListener(
            "beforeunload",
            function () {

                if (gameTimer) {

                    clearInterval(
                        gameTimer
                    );

                }


                stopWebcam();

            }
        );

    }
);