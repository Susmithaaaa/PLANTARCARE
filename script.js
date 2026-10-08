function toggleMenu() {

    const nav =
        document.getElementById("mainNav");

    if (nav) {

        nav.classList.toggle("open");

    }

}


// ============================================================
// LIVE BMI
// ============================================================

function calculateLiveBMI() {

    const heightInput =
        document.getElementById("heightInput");

    const weightInput =
        document.getElementById("weightInput");

    const bmiValue =
        document.getElementById("bmiValue");

    const bmiCategory =
        document.getElementById("bmiCategory");


    if (
        !heightInput ||
        !weightInput ||
        !bmiValue ||
        !bmiCategory
    ) {

        return;

    }


    const height =
        parseFloat(heightInput.value);

    const weight =
        parseFloat(weightInput.value);


    if (
        !height ||
        !weight ||
        height <= 0 ||
        weight <= 0
    ) {

        bmiValue.textContent = "--";

        bmiCategory.textContent =
            "Enter height & weight";

        return;

    }


    const bmi =
        weight /
        Math.pow(
            height / 100,
            2
        );


    bmiValue.textContent =
        bmi.toFixed(2);


    if (bmi < 18.5) {

        bmiCategory.textContent =
            "Underweight";

    }

    else if (bmi < 25) {

        bmiCategory.textContent =
            "Healthy Range";

    }

    else if (bmi < 30) {

        bmiCategory.textContent =
            "Overweight";

    }

    else {

        bmiCategory.textContent =
            "Higher BMI Range";

    }

}


// ============================================================
// TOE TAP GAME
// ============================================================

let tapCount = 0;


function tapGame() {

    tapCount++;


    const element =
        document.getElementById(
            "tapCount"
        );


    if (element) {

        element.textContent =
            tapCount;

    }

}


function resetTap() {

    tapCount = 0;


    const element =
        document.getElementById(
            "tapCount"
        );


    if (element) {

        element.textContent =
            "0";

    }

}


// ============================================================
// MEMORY GAME
// ============================================================

let memoryFirst = null;

let memoryLock = false;

let memoryMatches = 0;


function startMemory() {

    const board =
        document.getElementById(
            "memoryBoard"
        );


    if (!board) {

        return;

    }


    const symbols = [

        "🦶",
        "🦶",

        "💚",
        "💚",

        "⭐",
        "⭐",

        "💧",
        "💧"

    ];


    symbols.sort(
        () =>
            Math.random() - 0.5
    );


    memoryFirst = null;

    memoryLock = false;

    memoryMatches = 0;


    board.innerHTML = "";


    symbols.forEach(
        function(symbol) {

            const button =
                document.createElement(
                    "button"
                );


            button.className =
                "memory-card";


            button.dataset.symbol =
                symbol;


            button.textContent =
                "?";


            button.onclick =
                function() {

                    flipMemory(
                        button
                    );

                };


            board.appendChild(
                button
            );

        }
    );

}


function flipMemory(card) {

    if (
        memoryLock ||
        card.classList.contains(
            "matched"
        ) ||
        card === memoryFirst
    ) {

        return;

    }


    card.textContent =
        card.dataset.symbol;


    if (!memoryFirst) {

        memoryFirst =
            card;

        return;

    }


    memoryLock = true;


    if (
        memoryFirst.dataset.symbol ===
        card.dataset.symbol
    ) {

        memoryFirst.classList.add(
            "matched"
        );

        card.classList.add(
            "matched"
        );


        memoryMatches++;


        memoryFirst = null;

        memoryLock = false;

    }

    else {

        setTimeout(
            function() {

                memoryFirst.textContent =
                    "?";

                card.textContent =
                    "?";

                memoryFirst = null;

                memoryLock = false;

            },
            650
        );

    }

}


// ============================================================
// ALPHABET GAME
// ============================================================

let alphabetNext = 0;


function startAlphabet() {

    const board =
        document.getElementById(
            "alphabetBoard"
        );

    const message =
        document.getElementById(
            "alphabetMessage"
        );


    if (!board) {

        return;

    }


    alphabetNext = 0;

    board.innerHTML = "";


    "ABCDEFGH"
        .split("")
        .forEach(
            function(letter, index) {

                const button =
                    document.createElement(
                        "button"
                    );


                button.textContent =
                    letter;


                button.onclick =
                    function() {

                        if (
                            index ===
                            alphabetNext
                        ) {

                            button.classList.add(
                                "done"
                            );


                            alphabetNext++;


                            if (
                                alphabetNext === 8
                            ) {

                                message.textContent =
                                    "Completed!";

                            }

                            else {

                                message.textContent =
                                    "Next: " +
                                    String.fromCharCode(
                                        65 +
                                        alphabetNext
                                    );

                            }

                        }

                        else {

                            message.textContent =
                                "Try the next letter: " +
                                String.fromCharCode(
                                    65 +
                                    alphabetNext
                                );

                        }

                    };


                board.appendChild(
                    button
                );

            }
        );

}


// ============================================================
// PAGE LOAD
// ============================================================

document.addEventListener(
    "DOMContentLoaded",
    function() {

        calculateLiveBMI();


        const flashes =
            document.querySelectorAll(
                ".flash"
            );


        flashes.forEach(
            function(flash) {

                setTimeout(
                    function() {

                        flash.remove();

                    },
                    3500
                );

            }
        );


        startMemory();

        startAlphabet();

    }
);