//global variable
unsigned long tim, __tim, diff;                                 // 今回の立ち上がり時間tim, 前回の立ち上がり時間__tim, 時間差diff
char A[2][2][7][16], B[2][7], C[2];
char ai, aj, ak;
char swtE, swtI, flag;
char sig;

const char ham[3][7] = {{0, 0, 0, 1, 1, 1, 1},
                        {0, 1, 1, 0, 0, 1, 1},
                        {1, 0, 1, 0, 1, 0, 1}};                 // ハミング符号訂正の行列

const int span0 = 2000;                                         // 信号'0'の電圧立ち上がり理論値
const int span1 = 1000;                                         // 信号'1'の電圧立ち上がり理論値
const int span2 = 4000;                                         // 信号'2'の電圧立ち上がり理論値
const float uplimit = 1.1;                                      // 信号の曖昧さ許容
const float lowlimit = 0.9;

void dataedit() {
    char a, max, errnum;
    char i, j, k;
    char shell[4];
    char error[3];

    flag = 0;
    swtE = 1 - swtE;
    max = 0;
    errnum = 0;

    for(i = 0; i < 2; i++){                                     // 電圧立ち上がり x 16 x 7 x 2回で1バイトの情報
        for(j = 0; j < 7; j++){
            shell[0] = 0;
            shell[1] = 0;
            shell[2] = 0;
            shell[3] = 0;
            for(k = 0; k < 16; k++){
                a = A[swtI][i][j][k];                           // 信号の一時データ
                shell[a]++;
            }
            for(k = 1; k < 4; k++){
                if(shell[k] > shell[k - 1]){
                    max = k;                                    // 一番の候補を抽出，これがpython側の一番細かい一桁になる
                }
            }
            B[i][j] = max;
        }
        error[0] = 0;
        error[1] = 0;
        error[2] = 0;
        for(j = 0; j < 3; j++){                                 // ここにハミング訂正の行列積の計算
            for(k = 0; k < 7; k++){
        error[j] += B[i][k] * ham[j][k];
            }
        error[j] = error[j] % 2;
        }
        errnum = 4 * error[0] + 2 * error[1] + error[2];
        if(errnum != 0){
            B[i][errnum - 1] = 1 - B[i][errnum - 1];
        }
    }
}

void TKprint() {

}

void setup() {
    Serial.begin(9600);
    attachInterrupt(0, intrp, RISING);                          // 割り込み設定
    sig = 3;
    ai = 0, aj = 0;
    swtE = 0, swtI = 1, flag = 0;
}

void loop() {
    if(flag == 1){
        dataedit();
    TKprint();                                              // TK-80に入力とアドレスインクリメント
    }
}

void intrp() {
    tim = micros();
    diff = tim - __tim;
    __tim = tim;

    if(lowlimit * span0 < diff && diff < uplimit * span0){        // それぞれの信号の待ち時間が異なるため重みを考慮する
        A[swtI][ai][aj][ak] = 0;
        ak++;
        A[swtI][ai][aj][ak] = 0;
    }else if(lowlimit * span1 < diff && diff < uplimit * span1){
        A[swtI][ai][aj][ak] = 1;
    }else if(lowlimit * span2 < diff && diff < uplimit * span2){
        A[swtI][ai][aj][ak] = 2;
        ak++;
        A[swtI][ai][aj][ak] = 2;
        ak++;
        A[swtI][ai][aj][ak] = 2;
        ak++;
        A[swtI][ai][aj][ak] = 2;
    }else{
        A[swtI][ai][aj][ak] = 3;
    }

    if(ak >= 15){
        if(aj == 6){
            if(ai == 1){
                ai = 0;
                aj = 0;
                ak = 0;
                swtI = 1 - swtI;
                flag = 1;
            }else{
                aj = 0;
                ai++;
            }
        }else{
            ak = 0;
            aj++;
        }
    }else{
        ak++;
    }
}