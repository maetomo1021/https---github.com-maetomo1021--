document.addEventListener('DOMContentLoaded', (event) => {
    let score = 0;
    let timeLeft = 10;
    let countdownNumber = 3; // カウントダウン開始値
    let timer, countdownTimer;
    const scoreDisplay = document.getElementById('score');
    const timeDisplay = document.getElementById('time');
    const clickButton = document.getElementById('click-button');
    const startButton = document.getElementById('start-button');
    const countdownDisplay = document.createElement('div'); // カウントダウン表示用の要素
    countdownDisplay.id = 'countdown';
    countdownDisplay.style.fontSize = '100px';
    countdownDisplay.style.textAlign = 'center';
    document.body.insertBefore(countdownDisplay, document.body.firstChild); // ボディの最初に追加

    // 音声ファイルの準備
    const soundFiles = {
        1: new Audio('../music/Countdown03-mp3/Countdown03-1.mp3'),
        2: new Audio('../music/Countdown03-mp3/Countdown03-1.mp3'),
        3: new Audio('../music/Countdown03-mp3/Countdown03-1.mp3'),
        go: new Audio('../music/Countdown03-mp3/Countdown03-1.mp3')
    };

    function playSound(number) {
        if (soundFiles[number] && soundFiles[number].canPlayType) {
            soundFiles[number].play().catch(error => console.log('音声再生エラー:', error));
        }
    }

    // カウントダウンの開始
    function startCountdown() {
        countdownDisplay.textContent = countdownNumber;
        countdownTimer = setInterval(() => {
            playSound(countdownNumber); // 現在のカウントダウン値の音声を再生
            countdownDisplay.textContent = countdownNumber;
            countdownNumber--;

            if (countdownNumber < 0) {
                clearInterval(countdownTimer); // カウントダウン停止
                countdownDisplay.style.display = 'none'; // カウントダウンを非表示
                playSound('go'); // ゲーム開始音声
                startGame(); // ゲームを開始
            }
        }, 1000);
    }

    // クリックゲームの開始
    function startGame() {
        score = 0;
        timeLeft = 10;
        scoreDisplay.textContent = score;
        timeDisplay.textContent = timeLeft;
        clickButton.disabled = false;
        startButton.disabled = true;

        timer = setInterval(() => {
            timeLeft--;
            timeDisplay.textContent = timeLeft;
            if (timeLeft <= 0) {
                clearInterval(timer);
                clickButton.disabled = true;
                startButton.disabled = false;
                alert(`ゲーム終了! あなたの得点は ${score} です。`);
            }
        }, 1000);
    }

    // ゲーム再スタートのためのリセット
    function resetGame() {
        countdownNumber = 3; // カウントダウンのリセット
        countdownDisplay.textContent = countdownNumber;
        countdownDisplay.style.display = 'block'; // カウントダウン表示
        startCountdown(); // カウントダウンを開始
    }

    // スタートボタンを押すとカウントダウンを開始
    startButton.addEventListener('click', () => {
        resetGame();
    });

    // クリックボタンの得点増加処理
    clickButton.addEventListener('click', () => {
        if (timeLeft > 0) {
            score++;
            scoreDisplay.textContent = score;
        }
    });
});
