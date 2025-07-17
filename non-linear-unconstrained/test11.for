* SUBROUTINE TIUD11                ALL SYSTEMS                10/12/01
C PORTABILITY : ALL SYSTEMS
C 10/12/01 LU : ORIGINAL VERSION
*
* PURPOSE :
*  INITIAL VALUES OF VARIABLES FOR DENSE UNCONSTRAINED MINIMIZATION.
*
* PARAMETERS :
*  II  N  NUMBER OF VARIABLES.
*  RO  X(N)  VECTOR OF VARIABLES.
*  RO  FMIN  LOWER BOUND FOR THE OBJECTIVE FUNCTION.
*  RO  XMAX  MAXIMUM STEPSIZE.
*  II  NEXT  NUMBER OF THE TEST PROBLEM.
*  IO  IERR  ERROR INDICATOR.
*
      SUBROUTINE TIUD11(N,X,FMIN,XMAX,NEXT,IERR)
      INTEGER N,NEXT,IERR
      REAL*8 X(N),FMIN,XMAX
      REAL*8 P
      INTEGER I,L,M
      REAL*8 RPAR(10000)
      INTEGER IPAR(10),MM
      COMMON /EMPR11/ RPAR,IPAR,MM
      REAL*8 ETA9
      PARAMETER (ETA9=1.0D 120)
      FMIN=0.0D 0
      XMAX=1.0D 3
      IERR=0
      GO TO (10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,
     &  170,180,190,200,210,220,230,240,250,260,270,280,290,300,310,
     &  320,330,340,350,360,370,380,390,400,410,420,430,440,450,460,
     &  470,480,490,500,510,520,530,540,550,560,570,580),NEXT
C
C     ARWHEAD
C
   10 IF (N.LT.2) GO TO 999
      DO 11 I=1,N
      X(I)=1.0D 0
   11 CONTINUE
      RETURN
C
C     BDQRTIC
C
   20 IF (N.LT.5) GO TO 999
      DO 21 I=1,N
      X(I)=1.0D 0
   21 CONTINUE
      RETURN
C
C     BROYDN7D
C
   30 IF (N.LT.4) GO TO 999
      DO 31 I=1,N
      X(I)=1.0D 0
   31 CONTINUE
      FMIN=-ETA9
      RETURN
C
C     BRYBND
C
   40 IF (N.LT.7) GO TO 999
      DO 41 I=1,N
      X(I)=-1.0D 0
   41 CONTINUE
      RETURN
C
C     CHAINWOO
C
   50 IF (N.LT.4) GO TO 999
      N=N-MOD(N,2)
      X(1)=-3.0D 0
      X(2)=-1.0D 0
      X(3)=-3.0D 0
      X(4)=-1.0D 0
      DO 51 I=5,N
      X(I)=-2.0D 0
   51 CONTINUE
      RETURN
C
C     COSINE
C
   60 IF (N.LT.2) GO TO 999
      DO 61 I=1,N
      X(I)=1.0D 0
   61 CONTINUE
      FMIN=-ETA9
      RETURN
C
C     CRAGGLVY
C
   70 IF (N.LT.4) GO TO 999
      N=N-MOD(N,2)
      DO 71 I=1,N
      X(I)=2.0D 0
   71 CONTINUE
      X(1)=1.0D 0
      RETURN
C
C     CURLY10
C
   80 IF (N.LT.10) GO TO 999
      GO TO 101
C
C     CURLY20
C
   90 IF (N.LT.20) GO TO 999
      GO TO 101
C
C     CURLY30
C
  100 IF (N.LT.30) GO TO 999
  101 DO 102 I=1,N
      X(I)=1.0D-4/DBLE(N+1)
  102 CONTINUE
      FMIN=-ETA9
      RETURN
C
C     DIXMAANE
C
  110 IF (N.LT.6) GO TO 999
      IPAR(1)=1
      IPAR(2)=0
      IPAR(3)=0
      IPAR(4)=1
      RPAR(1)=1.0D 0
      RPAR(2)=0.0D 0
      RPAR(3)=1.25D-1
      RPAR(4)=1.25D-1
      GO TO 221
C
C     DIXMAANF
C
  120 IF (N.LT.6) GO TO 999
      IPAR(1)=1
      IPAR(2)=0
      IPAR(3)=0
      IPAR(4)=1
      RPAR(1)=1.0D 0
      RPAR(2)=6.25D-2
      RPAR(3)=6.25D-2
      RPAR(4)=6.25D-2
      GO TO 221
C
C     DIXMAANG
C
  130 IF (N.LT.6) GO TO 999
      IPAR(1)=1
      IPAR(2)=0
      IPAR(3)=0
      IPAR(4)=1
      RPAR(1)=1.0D 0
      RPAR(2)=1.25D-1
      RPAR(3)=1.25D-1
      RPAR(4)=1.25D-1
      GO TO 221
C
C     DIXMAANH
C
  140 IF (N.LT.6) GO TO 999
      IPAR(1)=1
      IPAR(2)=0
      IPAR(3)=0
      IPAR(4)=1
      RPAR(1)=1.0D 0
      RPAR(2)=2.6D-1
      RPAR(3)=2.6D-1
      RPAR(4)=2.6D-1
      GO TO 221
C
C     DIXMAANI
C
  150 IF (N.LT.6) GO TO 999
      IPAR(1)=2
      IPAR(2)=0
      IPAR(3)=0
      IPAR(4)=2
      RPAR(1)=1.0D 0
      RPAR(2)=0.0D 0
      RPAR(3)=1.25D-1
      RPAR(4)=1.25D-1
      GO TO 221
C
C     DIXMAANJ
C
  160 IF (N.LT.6) GO TO 999
      IPAR(1)=2
      IPAR(2)=0
      IPAR(3)=0
      IPAR(4)=2
      RPAR(1)=1.0D 0
      RPAR(2)=6.25D-2
      RPAR(3)=6.25D-2
      RPAR(4)=6.25D-2
      GO TO 221
C
C     DIXMAANK
C
  170 IF (N.LT.6) GO TO 999
      IPAR(1)=2
      IPAR(2)=0
      IPAR(3)=0
      IPAR(4)=2
      RPAR(1)=1.0D 0
      RPAR(2)=1.25D-1
      RPAR(3)=1.25D-1
      RPAR(4)=1.25D-1
      GO TO 221
C
C     DIXMAANL
C
  180 IF (N.LT.6) GO TO 999
      IPAR(1)=2
      IPAR(2)=0
      IPAR(3)=0
      IPAR(4)=2
      RPAR(1)=1.0D 0
      RPAR(2)=2.6D-1
      RPAR(3)=2.6D-1
      RPAR(4)=2.6D-1
      GO TO 221
C
C     DIXMAANM
C
  190 IF (N.LT.6) GO TO 999
      IPAR(1)=2
      IPAR(2)=1
      IPAR(3)=1
      IPAR(4)=2
      RPAR(1)=1.0D 0
      RPAR(2)=0.0D 0
      RPAR(3)=1.25D-1
      RPAR(4)=1.25D-1
      GO TO 221
C
C     DIXMAANN
C
  200 IF (N.LT.6) GO TO 999
      IPAR(1)=2
      IPAR(2)=1
      IPAR(3)=1
      IPAR(4)=2
      RPAR(1)=1.0D 0
      RPAR(2)=6.25D-2
      RPAR(3)=6.25D-2
      RPAR(4)=6.25D-2
      GO TO 221
C
C     DIXMAANO
C
  210 IF (N.LT.6) GO TO 999
      IPAR(1)=2
      IPAR(2)=1
      IPAR(3)=1
      IPAR(4)=2
      RPAR(1)=1.0D 0
      RPAR(2)=1.25D-1
      RPAR(3)=1.25D-1
      RPAR(4)=1.25D-1
      GO TO 221
C
C     DIXMAANP
C
  220 IF (N.LT.6) GO TO 999
      IPAR(1)=2
      IPAR(2)=1
      IPAR(3)=1
      IPAR(4)=2
      RPAR(1)=1.0D 0
      RPAR(2)=2.6D-1
      RPAR(3)=2.6D-1
      RPAR(4)=2.6D-1
  221 DO 222 I=1,N
      X(I)=2.0D 0
  222 CONTINUE
      FMIN=-ETA9
      RETURN
C
C     DQRTIC
C
  230 IF (N.LT.2) GO TO 999
      DO 231 I=1,N
      X(I)=2.0D 0
  231 CONTINUE
      RETURN
C
C     EDENSCH
C
  240 IF (N.LT.2) GO TO 999
      DO 241 I=1,N
      X(I)=0.0D 0
  241 CONTINUE
      RETURN
C
C     EG2
C
  250 IF (N.LT.2) GO TO 999
      DO 251 I=1,N
      X(I)=0.0D 0
  251 CONTINUE
      FMIN=-ETA9
      RETURN
C
C     ENGVAL1
C
  260 IF (N.LT.2) GO TO 999
      DO 261 I=1,N
      X(I)=2.0D 0
  261 CONTINUE
      RETURN
C
C     CHROSNB MODIFIED
C
  270 IF (N.LT.4) GO TO 999
      DO 271 I=1,N
      X(I)=-1.0D 0
  271 CONTINUE
      RETURN
C
C     ERRINROS MODIFIED
C
  280 IF (N.LT.4) GO TO 999
      DO 281 I=1,N
      X(I)=-1.0D 0
  281 CONTINUE
      RETURN
C
C     EXTROSNB
C
  290 IF (N.LT.2) GO TO 999
      DO 291 I=1,N
      X(I)=1.0D 0
  291 CONTINUE
      X(1)=-1.2D 0
      RETURN
C
C     FLETCBV3 MODIFIED
C
  300 IF (N.LT.2) GO TO 999
      RPAR(1)=1.0D 0
      RPAR(2)=1.0D 8
      GO TO 311
C
C     FLETCBV2
C
  310 IF (N.LT.2) GO TO 999
      RPAR(1)=1.0D 0
  311 P=1.0D 0/DBLE(N+1)
      DO 312 I=1,N
      X(I)=DBLE(I)*P
  312 CONTINUE
      FMIN=-ETA9
      RETURN
C
C     FLETCHCR
C
  320 IF (N.LT.2) GO TO 999
      DO 321 I=1,N
      X(I)=0.0D 0
  321 CONTINUE
      RETURN
C
C     FMINSRF2
C
  330 IF (N.LT.16) GO TO 999
      MM=INT(SQRT(DBLE(N)))
      IF (MOD(MM,2).EQ.0) MM=MM-1
      N=MM*MM
      DO 331 I=1,N
      X(I)=0.0D 0
  331 CONTINUE
      DO 332 I=1,MM
      X(I)=DBLE(I-1)*4.0D 0/DBLE(MM-1)+1.0D 0
      X((MM-1)*MM+I)=DBLE(I-1)*4.0D 0/DBLE(MM-1)+9.0D 0
  332 CONTINUE
      DO 333 I=2,MM-1
      X((I-1)*MM+MM)=DBLE(I-1)*8.0D 0/DBLE(MM-1)+1.0D 0
      X((I-1)*MM+1)=DBLE(I-1)*8.0D 0/DBLE(MM-1)+5.0D 0
  333 CONTINUE
      RETURN
C
C     FREUROTH
C
  340 IF (N.LT.2) GO TO 999
      DO 341 I=1,N
      X(I)=0.0D 0
  341 CONTINUE
      X(1)= 0.5D 0
      X(2)=-2.0D 0
      RETURN
C
C     GENHUMPS
C
  350 IF (N.LT.2) GO TO 999
      RPAR(1)=2.0D 1
      DO 351 I=1,N
      X(I)=-506.2D 0
  351 CONTINUE
      X(1)=-506.0D 0
      RETURN
C
C     GENROSE
C
  360 IF (N.LT.2) GO TO 999
      DO 361 I=1,N
      X(I)=DBLE(I)/DBLE(N+1)
  361 CONTINUE
      RETURN
C
C     INDEF MODIFIED
C
  370 IF (N.LT.2) GO TO 999
      RPAR(1)=0.5D 0
      DO 371 I=1,N
      X(I)=DBLE(I)/DBLE(N+1)
  371 CONTINUE
      FMIN=-ETA9
      RETURN
C
C     LIARWHD
C
  380 IF (N.LT.2) GO TO 999
      DO 381 I=1,N
      X(I)=4.0D 0
  381 CONTINUE
      RETURN
C
C     MOREBV DIFFERENT START POINT
C
  390 IF (N.LT.3) GO TO 999
      P=1.0D 0/DBLE(N+1)
      DO 391 I=1,N
      X(I)=0.5D 0
C      Q=P*DBLE(I)
C      X(I)=Q*(Q-1.0D 0)
  391 CONTINUE
      RETURN
C
C     NCB20 CORRECTED
C
  400 IF (N.LT.30) GO TO 999
      L=20
      M=10
      IPAR(1)=L
      IPAR(2)=M
      RPAR(1)=1.0D-4
      RPAR(2)=-4.0D 0/DBLE(L)
      DO 401 I=1,N-M
      X(I)=0.0D 0
  401 CONTINUE
      DO 402 I=N-M+1,N
      X(I)=1.0D 0
  402 CONTINUE
      FMIN=-ETA9
      RETURN
C
C     NCB20B CORRECTED
C
  410 IF (N.LT.20) GO TO 999
      L=20
      IPAR(1)=L
      RPAR(1)=1.0D 2
      RPAR(2)=-4.0D 0/DBLE(L)
      DO 411 I=1,N
      X(I)=0.0D 0
  411 CONTINUE
      FMIN=-ETA9
      RETURN
C
C     NONCVXUN
C
  420 CONTINUE
      IF (N.LT.12) GO TO 999
      DO 421 I=1,N
      X(I)=DBLE(I)
  421 CONTINUE
      RETURN
C
C     NONCVXU2
C
  430 CONTINUE
      IF (N.LT.12) GO TO 999
      DO 431 I=1,N
      X(I)=DBLE(I)
  431 CONTINUE
      RETURN
C
C     NONDIA
C
  440 CONTINUE
      IF (N.LT.2) GO TO 999
      DO 441 I=1,N
      X(I)=-1.0D 0
  441 CONTINUE
      RETURN
C
C     NONDQUAR
C
  450 CONTINUE
      IF (N.LT.2) GO TO 999
      DO 451 I=1,N
      IF (MOD(I,2).EQ.1) THEN
      X(I)= 1.0D 0
      ELSE
      X(I)=-1.0D 0
      ENDIF
  451 CONTINUE
      RETURN
C
C     PENALTY3
C
  460 IF (N.LT.3) GO TO 999
      P=1.0D 0/DBLE(N+1)
      DO 461 I=1,N
      X(I)=DBLE(I)*P
  461 CONTINUE
      RETURN
C
C     POWELLSG
C
  470 IF (N.LT.4) GO TO 999
      N=N-MOD(N,4)
      DO 471 I=1,N
      IF (MOD(I,4).EQ.1) THEN
      X(I)=3.0D 0
      ELSE IF (MOD(I,4).EQ.2) THEN
      X(I)=-1.0D 0
      ELSE IF (MOD(I,4).EQ.3) THEN
      X(I)=0.0D 0
      ELSE
      X(I)=1.0D 0
      ENDIF
  471 CONTINUE
      RETURN
C
C     SBRYBND
C
  480 IF (N.LT.7) GO TO 999
      DO 481 I=1,N
      RPAR(I)=EXP(6.0D 0*DBLE(I-1)/DBLE(N-1))
      X(I)=1.0D 0/RPAR(I)
  481 CONTINUE
      RETURN
C
C     SCHMVETT
C
  490 IF (N.LT.3) GO TO 999
      DO 491 I=1,N
      X(I)=3.0D 0
  491 CONTINUE
      FMIN=-ETA9
      RETURN
C
C     SCOSINE
C
  500 CONTINUE
      IF (N.LT.4) GO TO 999
      DO 501 I=1,N
      RPAR(I)=EXP(6.0D 0*DBLE(I-1)/DBLE(N-1))
      X(I)=1.0D 0/RPAR(I)
  501 CONTINUE
      FMIN=-ETA9
      RETURN
C
C     SINQUAD
C
  510 IF (N.LT.2) GO TO 999
      DO 511 I=1,N
      X(I)=1.0D-1
  511 CONTINUE
      RETURN
C
C     SPARSINE
C
  520 IF (N.LT.10) GO TO 999
      DO 521 I=1,N
      X(I)=0.5D 0
  521 CONTINUE
      RETURN
C
C     SPARSQUR
C
  530 IF (N.LT.10) GO TO 999
      DO 531 I=1,N
      X(I)=0.5D 0
  531 CONTINUE
      RETURN
C
C     SPMSRTLS
C
  540 IF (N.LT.7) GO TO 999
      N=N-MOD(N+2,3)
      DO 541 I=1,N
      RPAR(I)=SIN(DBLE(I)**2)
      X(I)=0.2D 0*RPAR(I)
  541 CONTINUE
      RETURN
C
C     SROSENBR
C
  550 IF (N.LT.2) GO TO 999
      N=N-MOD(N,2)
      DO 551 I=1,N
      IF (MOD(I,2).EQ.1) THEN
      X(I)=-1.2D 0
      ELSE
      X(I)= 1.0D 0
      ENDIF
  551 CONTINUE
      RETURN
C
C     TOINTGSS
C
  560 IF (N.LT.3) GO TO 999
      DO 561 I=1,N
      X(I)=3.0D 0
  561 CONTINUE
      RETURN
C
C     TQUARTIC MODIFIED
C
  570 IF (N.LT.2) GO TO 999
      DO 571 I=1,N
      X(I)=1.0D-1
  571 CONTINUE
C
C     WOODS
C
  580 IF (N.LT.4) GO TO 999
      DO 581 I=1,N
      IF (MOD(I,2).EQ.1) THEN
      X(I)=-3.0D 0
      ELSE
      X(I)=-1.0D 0
      ENDIF
  581 CONTINUE
      RETURN
  999 IERR=1
      RETURN
      END
* SUBROUTINE TIUX11                ALL SYSTEMS                10/12/01
C PORTABILITY : ALL SYSTEMS
C 10/12/01 LU : ORIGINAL VERSION
*
* PURPOSE :
*  DEFAULT DIMENSIONS OF THE PROBLEMS.
*
* PARAMETERS :
*  II  N  NUMBER OF VARIABLES.
*  II  NEXT  NUMBER OF THE TEST PROBLEM.
*
      SUBROUTINE TIUX11(N,NEXT)
      INTEGER N,NEXT
      GO TO (10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,
     &  170,180,190,200,210,220,230,240,250,260,270,280,290,300,310,
     &  320,330,340,350,360,370,380,390,400,410,420,430,440,450,460,
     &  470,480,490,500,510,520,530,540,550,560,570,580),NEXT
   10 N=5000
      RETURN
   20 N=5000
      RETURN
   30 N=2000
      RETURN
   40 N=5000
      RETURN
   50 N=1000
      RETURN
   60 N=5000
      RETURN
   70 N=5000
      RETURN
   80 N=1000
      RETURN
   90 N=1000
      RETURN
  100 N=1000
      RETURN
  110 N=3000
      RETURN
  120 N=3000
      RETURN
  130 N=3000
      RETURN
  140 N=3000
      RETURN
  150 N=3000
      RETURN
  160 N=3000
      RETURN
  170 N=3000
      RETURN
  180 N=3000
      RETURN
  190 N=3000
      RETURN
  200 N=3000
      RETURN
  210 N=3000
      RETURN
  220 N=3000
      RETURN
  230 N=5000
      RETURN
  240 N=5000
      RETURN
  250 N=1000
      RETURN
  260 N=5000
      RETURN
  270 N=1000
      RETURN
  280 N=1000
      RETURN
  290 N=1000
      RETURN
  300 N=1000
      RETURN
  310 N=1000
      RETURN
  320 N=1000
      RETURN
  330 N=5625
      RETURN
  340 N=5000
      RETURN
  350 N=1000
      RETURN
  360 N=1000
      RETURN
  370 N=1000
      RETURN
  380 N=5000
      RETURN
  390 N=5000
      RETURN
  400 N=1010
      RETURN
  410 N=1000
      RETURN
  420 N=1000
      RETURN
  430 N=1000
      RETURN
  440 N=5000
      RETURN
  450 N=5000
      RETURN
  460 N=1000
      RETURN
  470 N=5000
      RETURN
  480 N=1000
      RETURN
  490 N=5000
      RETURN
  500 N=1000
      RETURN
  510 N=5000
      RETURN
  520 N=1000
      RETURN
  530 N=1000
      RETURN
  540 N=5000
      RETURN
  550 N=5000
      RETURN
  560 N=5000
      RETURN
  570 N=5000
      RETURN
  580 N=4000
      RETURN
      END
* SUBROUTINE TFFU11                ALL SYSTEMS                10/12/01
C PORTABILITY : ALL SYSTEMS
C 10/12/01 LU : ORIGINAL VERSION
*
* PURPOSE :
*  VALUES OF MODEL FUNCTIONS FOR UNCONSTRAINED MINIMIZATION.
*  UNIVERSAL VERSION.
*
* PARAMETERS :
*  II  N  NUMBER OF VARIABLES.
*  RI  X(N)  VECTOR OF VARIABLES.
*  RO  F  VALUE OF THE MODEL FUNCTION.
*  II  NEXT  NUMBER OF THE TEST PROBLEM.
*
      SUBROUTINE TFFU11(N,X,F,NEXT)
      INTEGER N,NEXT
      REAL*8 X(N),F
      INTEGER I,I1,I2,I3,I4,I5,J,K,L,M
      REAL*8 A,B,C,D,E,P,Q,U,V,H,PI
      REAL*8 RPAR(10000)
      INTEGER IPAR(10),MM
      COMMON /EMPR11/ RPAR,IPAR,MM
      PI=3.14159265358979323846D 0
      F=0.0D 0
      GO TO (10,20,30,40,50,60,70,80,90,100,110,110,110,110,110,110,
     &  110,110,110,110,110,110,230,240,250,260,270,280,290,300,310,
     &  320,330,340,350,360,370,380,390,400,410,420,430,440,450,460,
     &  470,480,490,500,510,520,530,540,550,560,570,580),NEXT
   10 DO 11 I=1,N-1
      A=X(I)**2+X(N)**2
      F=F+A**2-4.0D 0*X(I)+3.0D 0
   11 CONTINUE
      RETURN
   20 DO 21 I=1,N-4
      A=3.0D 0-4.0D 0*X(I)
      B=X(I)**2+2.0D 0*X(I+1)**2+3.0D0*X(I+2)**2+4.0D 0*X(I+3)**2+
     & 5.0D 0*X(N)**2
      F=F+A**2+B**2
   21 CONTINUE
      RETURN
   30 P=7.0D 0/3.0D 0
      K=N/2
      DO 31 J=1,N
      A=(3.0D 0-2.0D 0*X(J))*X(J)+1.0D 0
      IF (J.GT.1) A=A-X(J-1)
      IF (J.LT.N) A=A-2.0D 0*X(J+1)
      F=F+ABS(A)**P
      IF (J.LE.K) THEN
      F=F+ABS(X(J)+X(J+K))**P
      ENDIF
   31 CONTINUE
      RETURN
   40 DO 43 I=1,N
      A=(2.0D 0+5.0D 0*X(I)**2)*X(I)+1.0D 0
      DO 41 J=MAX(1,I-5),MIN(N,I+1)
      IF (J.NE.I) A=A-X(J)*(1.0D 0+X(J))
   41 CONTINUE
      F=F+A*A
   43 CONTINUE
      RETURN
   50 F=1.0D 0
      DO 51 J=2,N-2,2
      A=X(J-1)**2-X(J)
      B=X(J-1)-1.0D 0
      C=X(J+1)**2-X(J+2)
      D=X(J+1)-1.0D 0
      U=X(J)+X(J+2)-2.0D 0
      V=X(J)-X(J+2)
      F=F+1.0D 2*A**2+B**2+9.0D 1*C**2+D**2+1.0D 1*U**2+0.1D 0*V**2
   51 CONTINUE
      RETURN
   60 DO 61 I=1,N-1
      A=X(I)**2-0.5D 0*X(I+1)
      F=F+COS(A)
   61 CONTINUE
      RETURN
   70 DO 71 J=2,N-2,2
      A=EXP(X(J-1))
      B=A-X(J)
      D=X(J)-X(J+1)
      P=X(J+1)-X(J+2)
      C=COS(P)
      Q=SIN(P)/C
      U=X(J-1)
      V=X(J+2)-1.0D 0
      F=F+B**4+1.0D 2*D**6+(Q+P)**4+U**8+V**2
   71 CONTINUE
      RETURN
   80 K=10
      GO TO 101
   90 K=20
      GO TO 101
  100 K=30
  101 DO 104 I=1,N
      A=0.0D 0
      DO 102 J=I,MIN(I+K,N)
      A=A+X(J)
  102 CONTINUE
      F=F+A*(A*(A**2-2.0D 1)-1.0D-1)
  104 CONTINUE
      RETURN
  110 M=N/3
      F=1.0D 0
      DO 111 I=1,N
      A=RPAR(1)*(DBLE(I)/DBLE(N))**IPAR(1)
      F=F+A*X(I)**2
  111 CONTINUE
      DO 112 I=1,N-1
      A=RPAR(2)*(DBLE(I)/DBLE(N))**IPAR(2)
      B=X(I+1)+X(I+1)**2
      F=F+A*X(I)**2*B**2
  112 CONTINUE
      DO 113 I=1,2*M
      A=RPAR(3)*(DBLE(I)/DBLE(N))**IPAR(3)
      F=F+A*X(I)**2*X(I+M)**4
  113 CONTINUE
      DO 114 I=1,M
      A=RPAR(4)*(DBLE(I)/DBLE(N))**IPAR(4)
      F=F+A*X(I)*X(I+2*M)
  114 CONTINUE
      RETURN
  230 DO 231 I=1,N
      F=F+(X(I)-DBLE(I))**4
  231 CONTINUE
      RETURN
  240 F=1.6D 1
      DO 241 I=1,N-1
      A=X(I)*X(I+1)-2.0D0*X(I+1)
      F=F+(X(I)-2.0D 0)**4+A**2+(X(I+1)+1.0D 0)**2
  241 CONTINUE
      RETURN
  250 DO 251 I=1,N-1
      A=X(1)+X(I)**2-1.0D 0
      F=F+SIN(A)
  251 CONTINUE
      F=F+0.5D0*SIN(X(N)**2)
      RETURN
  260 DO 261 I=1,N-1
      A=X(I)**2+X(I+1)**2
      F=F+A**2+3.0D 0-4.0D 0*X(I)
  261 CONTINUE
      RETURN
  270 DO 271 I=2,N
      A=1.6D 1*(1.5D 0+SIN(DBLE(I)))**2
      B=X(I-1)-X(I)**2
      F=F+A*B**2+(X(I)-1.0D 0)**2
  271 CONTINUE
      RETURN
  280 DO 281 I=2,N
      A=1.6D 1*(1.5D 0+SIN(DBLE(I)))**2
      B=X(I-1)-A*X(I)**2
      F=F+B**2+(X(I)-1.0D 0)**2
  281 CONTINUE
      RETURN
  290 F=(X(1)-1.0D 0)**2
      DO 291 I=2,N
      A=X(I)-X(I-1)**2
      F=F+1.0D 2*A**2
  291 CONTINUE
      RETURN
  300 H=1.0D 0/DBLE(N+1)**2
      P=1.0D 0/RPAR(2)
      F=0.5D 0*P*X(1)**2+0.5D 0*P*X(N)**2
      DO 301 I=1,N-1
      A=X(I)-X(I+1)
      F=F+0.5D 0*P*A**2
  301 CONTINUE
      A=1.0D 0+2.0D 0/H
      DO 302 I=1,N
      F=F-P*(A*1.0D 2*SIN(X(I)/1.0D 2)+RPAR(1)*COS(X(I))/H)
  302 CONTINUE
      RETURN
  310 H=1.0D 0/DBLE(N+1)**2
      F=0.5D 0*X(1)**2+0.5D 0*X(N)**2
      DO 311 I=1,N-1
      A=X(I)-X(I+1)
      F=F+0.5D 0*A**2
  311 CONTINUE
      A=2.0D 0*H
      DO 312 I=1,N-1
      F=F-A*X(I)-RPAR(1)*COS(X(I))*H
  312 CONTINUE
      A=1.0D 0+2.0D 0*H
      F=F-A*X(N)-RPAR(1)*COS(X(N))*H
      RETURN
  320 DO 321 I=1,N-1
      A=X(I)*(X(I)+1.0D 0)-X(I+1)-1.0D 0
      F=F+1.0D 2*A**2
  321 CONTINUE
      RETURN
  330 P=DBLE(MM-1)**2
      L=0
      DO 332 I=1,MM-1
      DO 331 J=1,MM-1
      A=X(L+J)-X(L+MM+J+1)
      B=X(L+MM+J)-X(L+J+1)
      C=0.5D 0*P*(A**2+B**2)+1.0D 0
      F=F+SQRT(C)/P
  331 CONTINUE
      L=L+MM
  332 CONTINUE
      L=MM*(MM-1)/2
      F=F+X(L)**2/DBLE(MM**2)
      RETURN
  340 DO 341 I=1,N-1
      A=X(I)+((5.0D 0-X(I+1))*X(I+1)-2.0D 0)*X(I+1)-1.3D 1
      F=F+A**2
      A=X(I)+((X(I+1)+1.0D 0)*X(I+1)-1.4D 1)*X(I+1)-2.9D 1
      F=F+A**2
  341 CONTINUE
      RETURN
  350 P=RPAR(1)
      DO 351 I=1,N-1
      A=SIN(P*X(I))
      B=SIN(P*X(I+1))
      F=F+A**2*B**2+5.0D-2*(X(I)**2+X(I+1)**2)
  351 CONTINUE
      RETURN
  360 F=1.0D 0
      DO 361 I=2,N
      A=X(I)-X(I-1)**2
      F=F+1.0D 2*A**2+(X(I)-1.0D 0)**2
  361 CONTINUE
      RETURN
  370 DO 371 I=1,N
      F=F+1.0D 2*SIN(X(I)/1.0D 2)
  371 CONTINUE
      DO 372 I=2,N-1
      A=2.0D 0*X(I)-X(N)-X(1)
      F=F+RPAR(1)*COS(A)
  372 CONTINUE
      RETURN
  380 DO 381 I=1,N
      A=X(I)**2-X(1)
      F=F+4.0D 0*A**2+(X(I)-1.0D 0)**2
  381 CONTINUE
      RETURN
  390 P=1.0D 0/DBLE(N+1)
      Q=0.5D 0*P**2
      DO 391 I=1,N
      A=2.0D 0*X(I)+Q*(X(I)+DBLE(I)*P+1.0D 0)**3
      IF (I.GT.1) A=A-X(I-1)
      IF (I.LT.N) A=A-X(I+1)
      F=F+A**2
  391 CONTINUE
      RETURN
  400 L=IPAR(1)
      M=IPAR(2)
      F=2.0D 0
      DO 403 I=1,N-L-M
      C=1.0D 1/DBLE(I)
      D=0.0D 0
      DO 401 J=1,L
      A=X(I+J-1)
      B=1.0D 0+A*A
      D=D+A/B
      F=F+RPAR(2)*A
  401 CONTINUE
      F=F+C*D*D
  403 CONTINUE
      DO 404 I=1,N-M
      F=F+X(I)**4+2.0D 0
  404 CONTINUE
      DO 405 I=1,M
      F=F+RPAR(1)*(X(I)*X(I+M)*X(I+N-M)+2.0D 0*X(I+N-M)**2)
  405 CONTINUE
      RETURN
  410 L=IPAR(1)
      DO 413 I=1,N-L+1
      C=1.0D 1/DBLE(I)
      D=0.0D 0
      DO 411 J=1,L
      A=X(I+J-1)
      B=1.0D 0+A*A
      D=D+A/B
      F=F+RPAR(2)*A
  411 CONTINUE
      F=F+C*D*D
  413 CONTINUE
      DO 414 I=1,N
      F=F+RPAR(1)*X(I)**4+2.0D 0
  414 CONTINUE
      RETURN
  420 DO 421 I=1,N
      K=MOD(2*I-1,N)
      L=MOD(3*I-1,N)
      A=X(I)+X(K+1)+X(L+1)
      F=F+A**2+4.0D 0*COS(A)
  421 CONTINUE
      RETURN
  430 DO 431 I=1,N
      K=MOD(3*I-2,N)
      L=MOD(7*I-3,N)
      A=X(I)+X(K+1)+X(L+1)
      F=F+A**2+4.0D 0*COS(A)
  431 CONTINUE
      RETURN
  440 F=(X(1)-1.0D 0)**2
      DO 441 I=2,N
      A=X(1)-X(I-1)**2
      F=F+1.0D 2*A**2
  441 CONTINUE
      RETURN
  450 A=X(1)-X(2)
      B=X(N-1)-X(N)
      F=A**2+B**2
      DO 451 I=1,N-2
      A=X(I)+X(I+1)+X(N)
      F=F+A**4
  451 CONTINUE
      RETURN
  460 A=1.0D 0
      B=0.0D 0
      C=0.0D 0
      D=0.0D 0
      F=0.0D 0
      U=EXP(X(N))
      V=EXP(X(N-1))
      DO 461 J=1,N
      IF (J.LE.N/2) F=F+(X(J)-1.0D 0)**2
      IF (J.LE.N-2) THEN
      B=B+(X(J)+2.0D 0*X(J+1)+1.0D 1*X(J+2)-1.0D 0)**2
      C=C+(2.0D 0*X(J)+X(J+1)-3.0D 0)**2
      ENDIF
      D=D+X(J)**2-DBLE(N)
  461 CONTINUE
      F=F+A*(1.0D 0+U*B+B*C+V*C)+D**2
      RETURN
  470 DO 471 J=1,N-3,4
      A=X(J)+1.0D 1*X(J+1)
      B=X(J+2)-X(J+3)
      C=X(J+1)-2.0D 0*X(J+2)
      D=X(J)-X(J+3)
      F=F+A**2+5.0D 0*B**2+C**4+1.0D 1*D**4
  471 CONTINUE
      RETURN
  480 DO 483 I=1,N
      P=RPAR(I)
      A=(2.0D 0+5.0D 0*(P*X(I))**2)*P*X(I)+1.0D 0
      DO 481 J=MAX(1,I-5),MIN(N,I+1)
      IF (J.NE.I) THEN
      Q=RPAR(J)
      A=A-Q*X(J)*(1.0D 0+Q*X(J))
      ENDIF
  481 CONTINUE
      F=F+A*A
  483 CONTINUE
      RETURN
  490 DO 491 I=1,N-2
      A=X(I)-X(I+1)
      B=0.5D 0*(PI*X(I+1)+X(I+2))
      D=X(I)+X(I+2)
      E=D/X(I+1)-2.0D 0
      U=EXP(-E**2)
      V=1.0D 0+A**2
      F=F-1.0D 0/V-SIN(B)-U
  491 CONTINUE
      RETURN
  500 DO 501 I=1,N-1
      P=RPAR(I)
      Q=RPAR(I+1)
      A=(P*X(I))**2-0.5D 0*Q*X(I+1)
      F=F+COS(A)
  501 CONTINUE
      RETURN
  510 A=X(1)-1.0D 0
      B=X(N)**2-X(1)**2
      F=A**4+B**2
      DO 511 I=2,N-1
      A=X(I)-X(N)
      B=SIN(A)+X(I)**2-X(1)**2
      F=F+B**2
  511 CONTINUE
      RETURN
  520 DO 521 I=1,N
      I1=MOD(2*I-1,N)+1
      I2=MOD(3*I-1,N)+1
      I3=MOD(5*I-1,N)+1
      I4=MOD(7*I-1,N)+1
      I5=MOD(11*I-1,N)+1
      A=SIN(X(I))+SIN(X(I1))+SIN(X(I2))+SIN(X(I3))+SIN(X(I4))+SIN(X(I5))
      F=F+DBLE(I)*A*A
  521 CONTINUE
      F=5.0D-1*F
      RETURN
  530 DO 531 I=1,N
      I1=MOD(2*I-1,N)+1
      I2=MOD(3*I-1,N)+1
      I3=MOD(5*I-1,N)+1
      I4=MOD(7*I-1,N)+1
      I5=MOD(11*I-1,N)+1
      A=5.0D-1*(X(I)**2+X(I1)**2+X(I2)**2+X(I3)**2+X(I4)**2+X(I5)**2)
      F=F+DBLE(I)*A*A
  531 CONTINUE
      F=5.0D-1*F
      RETURN
  540 M=(N+2)/3
      DO 542 I=1,M
      J=3*(I-1)+1
      DO 541 K=1,5
      IF (MOD(K,5).EQ.1) THEN
      IF (I.GT.2) THEN
      A=X(J-4)*X(J-1)-RPAR(J-4)*RPAR(J-1)
      F=F+A*A
      ENDIF
      ELSE IF(MOD(K,5).EQ.2) THEN
      IF (I.GT.1) THEN
      A=X(J-3)*X(J-1)+X(J-1)*X(J)-RPAR(J-3)*RPAR(J-1)-RPAR(J-1)*RPAR(J)
      F=F+A*A
      ENDIF
      ELSE IF(MOD(K,5).EQ.3) THEN
      IF (I.GT.1) THEN
      A=X(J-2)*X(J-1)-RPAR(J-2)*RPAR(J-1)
      F=F+A*A
      ENDIF
      A=X(J)*X(J)-RPAR(J)*RPAR(J)
      F=F+A*A
      IF (I.LT.M) THEN
      A=X(J+2)*X(J+1)-RPAR(J+2)*RPAR(J+1)
      F=F+A*A
      ENDIF
      ELSE IF(MOD(K,5).EQ.4) THEN
      IF (I.LT.M) THEN
      A=X(J+3)*X(J+1)+X(J+1)*X(J)-RPAR(J+3)*RPAR(J+1)-RPAR(J+1)*RPAR(J)
      F=F+A*A
      ENDIF
      ELSE
      IF (I.LT.M-1) THEN
      A=X(J+4)*X(J+1)-RPAR(J+4)*RPAR(J+1)
      F=F+A*A
      ENDIF
      ENDIF
  541 CONTINUE
  542 CONTINUE
      RETURN
  550 DO 551 I=2,N,2
      A=X(I)-X(I-1)**2
      F=F+1.0D 2*A**2+(X(I-1)-1.0D 0)**2
  551 CONTINUE
      RETURN
  560 DO 561 I=1,N-2
      A=1.0D 1/DBLE(N+2)+X(I+2)**2
      B=X(I)-X(I+1)
      C=1.0D-1+X(I+2)**2
      D=-B**2/C
      E=EXP(D)
      F=F+A*(2.0D 0-E)
  561 CONTINUE
      RETURN
  570 A=X(1)-1.0D 0
      F=A**2
      DO 571 I=1,N-1
      A=X(1)**2-X(I+1)**2
      F=F+A**2
  571 CONTINUE
      RETURN
  580 DO 581 J=2,N-2,4
      A=X(J-1)**2-X(J)
      B=X(J-1)-1.0D 0
      C=X(J+1)**2-X(J+2)
      D=X(J)+X(J+2)-2.0D 0
      E=X(J)-X(J+2)
      U=X(J+1)-1.0D 0
      F=F+1.0D 2*A**2+B**2+9.0D 1*C**2+1.0D 1*D**2+1.0D-1*E**2+U**2
  581 CONTINUE
      RETURN
      END
* SUBROUTINE TFGU11                ALL SYSTEMS                10/12/01
C PORTABILITY : ALL SYSTEMS
C 10/12/01 LU : ORIGINAL VERSION
*
* PURPOSE :
*  GRADIENTS OF MODEL FUNCTIONS FOR UNCONSTRAINED MINIMIZATION.
*  UNIVERSAL VERSION.
*
* PARAMETERS :
*  II  N  NUMBER OF VARIABLES.
*  RI  X(N)  VECTOR OF VARIABLES.
*  RI  G(N)  GRADIENG OF THE MODEL FUNCTION.
*  II  NEXT  NUMBER OF THE TEST PROBLEM.
*
      SUBROUTINE TFGU11(N,X,G,NEXT)
      INTEGER N,NEXT
      REAL*8 X(N),G(N)
      INTEGER I,I1,I2,I3,I4,I5,J,K,L,M
      REAL*8 A,B,C,D,E,P,Q,U,V,H,PI
      REAL*8 RPAR(10000)
      INTEGER IPAR(10),MM
      COMMON /EMPR11/ RPAR,IPAR,MM
      PI=3.14159265358979323846D 0
      CALL UXVSET(N,0.0D 0,G)
      GO TO (10,20,30,40,50,60,70,80,90,100,110,110,110,110,110,110,
     &  110,110,110,110,110,110,230,240,250,260,270,280,290,300,310,
     &  320,330,340,350,360,370,380,390,400,410,420,430,440,450,460,
     &  470,480,490,500,510,520,530,540,550,560,570,580),NEXT
   10 DO 11 I=1,N-1
      A=X(I)**2+X(N)**2
      G(I)=4.0D 0*A*X(I)-4.0D 0
      G(N)=G(N)+4.0D 0*A*X(N)
   11 CONTINUE
      RETURN
   20 DO 21 I=1,N-4
      A=3.0D 0-4.0D 0*X(I)
      B=X(I)**2+2.0D 0*X(I+1)**2+3.0D0*X(I+2)**2+4.0D 0*X(I+3)**2+
     & 5.0D 0*X(N)**2
      G(I)=G(I)+4.0D 0*B*X(I)-8.0D 0*A
      G(I+1)=G(I+1)+8.0D 0*B*X(I+1)
      G(I+2)=G(I+2)+1.2D 1*B*X(I+2)
      G(I+3)=G(I+3)+1.6D 1*B*X(I+3)
      G(N)=G(N)+2.0D 1*B*X(N)
   21 CONTINUE
      RETURN
   30 P=7.0D 0/3.0D 0
      K=N/2
      DO 31 J=1,N
      A=(3.0D 0-2.0D 0*X(J))*X(J)+1.0D 0
      IF (J.GT.1) A=A-X(J-1)
      IF (J.LT.N) A=A-2.0D 0*X(J+1)
      B=P*ABS(A)**(P-1.0D 0)*SIGN(1.0D 0,A)
      G(J)=G(J)+B*(3.0D 0-4.0D 0*X(J))
      IF (J.GT.1) G(J-1)=G(J-1)-B
      IF (J.LT.N) G(J+1)=G(J+1)-2.0D 0*B
      IF (J.LE.K) THEN
      A=X(J)+X(J+K)
      B=P*ABS(A)**(P-1.0D 0)*SIGN(1.0D 0,A)
      G(J)=G(J)+B
      G(J+K)=G(J+K)+B
      ENDIF
   31 CONTINUE
      RETURN
   40 DO 43 I=1,N
      A=(2.0D 0+5.0D 0*X(I)**2)*X(I)+1.0D 0
      DO 41 J=MAX(1,I-5),MIN(N,I+1)
      IF (J.NE.I) A=A-X(J)*(1.0D 0+X(J))
   41 CONTINUE
      G(I)=G(I)+2.0D 0*A*(2.0D 0+1.5D 1*X(I)**2)
      DO 42 J=MAX(1,I-5),MIN(N,I+1)
      IF (J.NE.I) G(J)=G(J)-2.0D 0*A*(1.0D 0+2.0D 0*X(J))
   42 CONTINUE
   43 CONTINUE
      RETURN
   50 DO 51 J=2,N-2,2
      A=X(J-1)**2-X(J)
      B=X(J-1)-1.0D 0
      C=X(J+1)**2-X(J+2)
      D=X(J+1)-1.0D 0
      U=X(J)+X(J+2)-2.0D 0
      V=X(J)-X(J+2)
      G(J-1)=G(J-1)+4.0D 2*X(J-1)*A+2.0D 0*B
      G(J)=G(J)-2.0D 2*A+2.0D 1*U+0.2D 0*V
      G(J+1)=G(J+1)+3.6D 2*X(J+1)*C+2.0D 0*D
      G(J+2)=G(J+2)-1.8D 2*C+2.0D 1*U-0.2D 0*V
   51 CONTINUE
      RETURN
   60 DO 61 I=1,N-1
      A=X(I)**2-0.5D 0*X(I+1)
      B=SIN(A)
      G(I)=G(I)-2.0D 0*B*X(I)
      G(I+1)=G(I+1)+0.5D 0*B
   61 CONTINUE
      RETURN
   70 DO 71 J=2,N-2,2
      A=EXP(X(J-1))
      B=A-X(J)
      D=X(J)-X(J+1)
      P=X(J+1)-X(J+2)
      C=COS(P)
      Q=SIN(P)/C
      U=X(J-1)
      V=X(J+2)-1.0D 0
      B=4.0D 0*B**3
      D=6.0D 2*D**5
      E=4.0D 0*(Q+P)**3
      Q=E*(1.0D 0+1.0D 0/C**2)
      G(J-1)=G(J-1)+A*B+8.0D 0*U**7
      G(J)=G(J)+D-B
      G(J+1)=G(J+1)+Q-D
      G(J+2)=G(J+2)+2.0D 0*V-Q
   71 CONTINUE
      RETURN
   80 K=10
      GO TO 101
   90 K=20
      GO TO 101
  100 K=30
  101 DO 104 I=1,N
      A=0.0D 0
      DO 102 J=I,MIN(I+K,N)
      A=A+X(J)
  102 CONTINUE
      B=4.0D 0*A*(A**2-1.0D 1)-1.0D-1
      DO 103 J=I,MIN(I+K,N)
      G(J)=G(J)+B
  103 CONTINUE
  104 CONTINUE
      RETURN
  110 M=N/3
      DO 111 I=1,N
      A=RPAR(1)*(DBLE(I)/DBLE(N))**IPAR(1)
      G(I)=G(I)+2.0D 0*A*X(I)
  111 CONTINUE
      DO 112 I=1,N-1
      A=RPAR(2)*(DBLE(I)/DBLE(N))**IPAR(2)
      B=X(I+1)+X(I+1)**2
      G(I)=G(I)+2.0D 0*A*B**2*X(I)
      G(I+1)=G(I+1)+A*B*X(I)**2*(4.0D 0*X(I+1)+2.0D 0)
  112 CONTINUE
      DO 113 I=1,2*M
      A=RPAR(3)*(DBLE(I)/DBLE(N))**IPAR(3)
      G(I)=G(I)+2.0D 0*A*X(I)*X(I+M)**4
      G(I+M)=G(I+M)+4.0D 0*A*X(I)**2*X(I+M)**3
  113 CONTINUE
      DO 114 I=1,M
      A=RPAR(4)*(DBLE(I)/DBLE(N))**IPAR(4)
      G(I)=G(I)+A*X(I+2*M)
      G(I+2*M)=G(I+2*M)+A*X(I)
  114 CONTINUE
      RETURN
  230 DO 231 I=1,N
      G(I)=G(I)+4.0D 0*(X(I)-DBLE(I))**3
  231 CONTINUE
      RETURN
  240 DO 241 I=1,N-1
      A=X(I)*X(I+1)-2.0D0*X(I+1)
      G(I)=G(I)+4.0D 0*(X(I)-2.0D 0)**3+2.0D 0*A*X(I+1)
      G(I+1)=G(I+1)+2.0D 0*A*(X(I)-2.0D 0)+2.0D 0*(X(I+1)+1.0D 0)
  241 CONTINUE
      RETURN
  250 DO 251 I=1,N-1
      A=X(1)+X(I)**2-1.0D 0
      B=COS(A)
      G(1)=G(1)+B
      G(I)=G(I)+2.0D 0*X(I)*B
  251 CONTINUE
      G(N)=G(N)+COS(X(N)**2)*X(N)
      RETURN
  260 DO 261 I=1,N-1
      A=X(I)**2+X(I+1)**2
      G(I)=G(I)+4.0D 0*A*X(I)-4.0D 0
      G(I+1)=G(I+1)+4.0D 0*A*X(I+1)
  261 CONTINUE
      RETURN
  270 DO 271 I=2,N
      A=1.6D 1*(1.5D 0+SIN(DBLE(I)))**2
      B=X(I-1)-X(I)**2
      G(I)=G(I)-4.0D 0*A*B*X(I)+2.0D 0*(X(I)-1.0D0)
      G(I-1)=G(I-1)+2.0D 0*A*B
  271 CONTINUE
      RETURN
  280 DO 281 I=2,N
      A=1.6D 1*(1.5D 0+SIN(DBLE(I)))**2
      B=X(I-1)-A*X(I)**2
      G(I)=G(I)-4.0D 0*A*B*X(I)+2.0D 0*(X(I)-1.0D0)
      G(I-1)=G(I-1)+2.0D 0*B
  281 CONTINUE
      RETURN
  290 G(1)=2.0D 0*(X(1)-1.0D 0)
      DO 291 I=2,N
      A=X(I)-X(I-1)**2
      G(I)=G(I)+2.0D 2*A
      G(I-1)=G(I-1)-4.0D 2*A*X(I-1)
  291 CONTINUE
      RETURN
  300 H=1.0D 0/DBLE(N+1)**2
      P=1.0D 0/RPAR(2)
      G(1)=P*X(1)
      G(N)=P*X(N)
      DO 301 I=1,N-1
      A=X(I)-X(I+1)
      G(I)=G(I)+P*A
      G(I+1)=G(I+1)-P*A
  301 CONTINUE
      A=1.0D 0+2.0D 0/H
      DO 302 I=1,N
      G(I)=G(I)-P*(A*COS(X(I)/1.0D 2)-RPAR(1)*SIN(X(I))/H)
  302 CONTINUE
      RETURN
  310 H=1.0D 0/DBLE(N+1)**2
      G(1)=X(1)
      G(N)=X(N)
      DO 311 I=1,N-1
      A=X(I)-X(I+1)
      G(I)=G(I)+A
      G(I+1)=G(I+1)-A
  311 CONTINUE
      A=2.0D 0*H
      DO 312 I=1,N-1
      G(I)=G(I)-A+RPAR(1)*SIN(X(I))*H
  312 CONTINUE
      A=1.0D 0+2.0D 0*H
      G(N)=G(N)-A+RPAR(1)*SIN(X(I))*H
      RETURN
  320 DO 321 I=1,N-1
      A=X(I)*(X(I)+1.0D 0)-X(I+1)-1.0D 0
      G(I)=G(I)+2.0D 2*A*(2.0D 0*X(I)+1.0D 0)
      G(I+1)=G(I+1)-2.0D 2*A
  321 CONTINUE
      RETURN
  330 P=DBLE(MM-1)**2
      L=0
      DO 332 I=1,MM-1
      DO 331 J=1,MM-1
      A=X(L+J)-X(L+MM+J+1)
      B=X(L+MM+J)-X(L+J+1)
      C=0.5D 0*P*(A**2+B**2)+1.0D 0
      D=0.5D 0/SQRT(C)
      G(L+J)=G(L+J)+D*A
      G(L+MM+J+1)=G(L+MM+J+1)-D*A
      G(L+MM+J)=G(L+MM+J)+D*B
      G(L+J+1)=G(L+J+1)-D*B
  331 CONTINUE
      L=L+MM
  332 CONTINUE
      L=MM*(MM-1)/2
      G(L)=G(L)+2.0D 0*X(L)/DBLE(MM**2)
      RETURN
  340 DO 341 I=1,N-1
      A=X(I)+((5.0D 0-X(I+1))*X(I+1)-2.0D 0)*X(I+1)-1.3D 1
      G(I)=G(I)+A
      G(I+1)=G(I+1)+(1.0D 1*X(I+1)-3.0D 0*X(I+1)**2-2.0D 0)*A
      A=X(I)+((X(I+1)+1.0D 0)*X(I+1)-1.4D 1)*X(I+1)-2.9D 1
      G(I)=G(I)+A
      G(I+1)=G(I+1)+(3.0D 0*X(I+1)**2+2.0D 0*X(I+1)-1.4D 1)*A
  341 CONTINUE
      RETURN
  350 P=RPAR(1)
      DO 351 I=1,N-1
      A=SIN(P*X(I))
      B=SIN(P*X(I+1))
      G(I)=G(I)+2.0D 0*P*A*B**2*COS(P*X(I))+1.0D-1*X(I)
      G(I+1)=G(I+1)+2.0D 0*P*A**2*B*COS(P*X(I+1))+1.0D-1*X(I+1)
  351 CONTINUE
      RETURN
  360 DO 361 I=2,N
      A=X(I)-X(I-1)**2
      G(I)=G(I)+2.0D 2*A+2.0D 0*(X(I)-1.0D 0)
      G(I-1)=G(I-1)-4.0D 2*A*X(I-1)
  361 CONTINUE
      RETURN
  370 DO 371 I=1,N
      G(I)=G(I)+COS(X(I)/1.0D 2)
  371 CONTINUE
      DO 372 I=2,N-1
      A=2.0D 0*X(I)-X(N)-X(1)
      B=RPAR(1)*SIN(A)
      G(I)=G(I)-2.0D 0*B
      G(1)=G(1)+B
      G(N)=G(N)+B
  372 CONTINUE
      RETURN
  380 DO 381 I=1,N
      A=X(I)**2-X(1)
      G(I)=G(I)+1.6D 1*A*X(I)+2.0D 0*(X(I)-1.0D 0)
      G(1)=G(1)-8.0D 0*A
  381 CONTINUE
      RETURN
  390 P=1.0D 0/DBLE(N+1)
      Q=0.5D 0*P**2
      DO 391 I=1,N
      A=2.0D 0*X(I)+Q*(X(I)+DBLE(I)*P+1.0D 0)**3
      IF (I.GT.1) A=A-X(I-1)
      IF (I.LT.N) A=A-X(I+1)
      G(I)=G(I)+A*(4.0D 0+6.0D 0*Q*(X(I)+DBLE(I)*P+1.0D 0)**2)
      IF(I.GT.1) G(I-1)=G(I-1)-2.0D 0*A
      IF(I.LT.N) G(I+1)=G(I+1)-2.0D 0*A
  391 CONTINUE
      RETURN
  400 L=IPAR(1)
      M=IPAR(2)
      DO 403 I=1,N-L-M
      C=1.0D 1/DBLE(I)
      D=0.0D 0
      DO 401 J=1,L
      A=X(I+J-1)
      B=1.0D 0+A*A
      D=D+A/B
      G(I+J-1)=G(I+J-1)+RPAR(2)
  401 CONTINUE
      DO 402 J=1,L
      A=X(I+J-1)
      B=1.0D 0+A*A
      G(I+J-1)=G(I+J-1)+2.0D 0*C*D*(1-A*A)/B**2
  402 CONTINUE
  403 CONTINUE
      DO 404 I=1,N-M
      G(I)=G(I)+4.0D 0*X(I)**3
  404 CONTINUE
      DO 405 I=1,M
      G(I)=G(I)+RPAR(1)*X(I+M)*X(I+N-M)
      G(I+M)=G(I+M)+RPAR(1)*X(I)*X(I+N-M)
      G(I+N-M)=G(I+N-M)+RPAR(1)*(X(I)*X(I+M)+4.0D 0*X(I+N-M))
  405 CONTINUE
      RETURN
  410 L=IPAR(1)
      DO 413 I=1,N-L+1
      C=1.0D 1/DBLE(I)
      D=0.0D 0
      DO 411 J=1,L
      A=X(I+J-1)
      B=1.0D 0+A*A
      D=D+A/B
      G(I+J-1)=G(I+J-1)+RPAR(2)
  411 CONTINUE
      DO 412 J=1,L
      A=X(I+J-1)
      B=1.0D 0+A*A
      G(I+J-1)=G(I+J-1)+2.0D 0*C*D*(1-A*A)/B**2
  412 CONTINUE
  413 CONTINUE
      DO 414 I=1,N
      G(I)=G(I)+4.0D 0*RPAR(1)*X(I)**3
  414 CONTINUE
      RETURN
  420 DO 421 I=1,N
      K=MOD(2*I-1,N)
      L=MOD(3*I-1,N)
      A=X(I)+X(K+1)+X(L+1)
      B=SIN(A)
      G(I)=G(I)+2.0D 0*A-4.0D 0*B
      G(K+1)=G(K+1)+2.0D 0*A-4.0D 0*B
      G(L+1)=G(L+1)+2.0D 0*A-4.0D 0*B
  421 CONTINUE
      RETURN
  430 DO 431 I=1,N
      K=MOD(3*I-2,N)
      L=MOD(7*I-3,N)
      A=X(I)+X(K+1)+X(L+1)
      B=SIN(A)
      G(I)=G(I)+2.0D 0*A-4.0D 0*B
      G(K+1)=G(K+1)+2.0D 0*A-4.0D 0*B
      G(L+1)=G(L+1)+2.0D 0*A-4.0D 0*B
  431 CONTINUE
      RETURN
  440 G(1)=2.0D 0*(X(1)-1.0D 0)
      DO 441 I=2,N
      A=X(1)-X(I-1)**2
      G(1)=G(1)+2.0D 2*A
      G(I-1)=G(I-1)-4.0D 2*A*X(I-1)
  441 CONTINUE
      RETURN
  450 A=X(1)-X(2)
      B=X(N-1)-X(N)
      G(1)=2.0D 0*A
      G(2)=-2.0D 0*A
      G(N-1)=2.0D 0*B
      G(N)=-2.0D 0*B
      DO 451 I=1,N-2
      A=X(I)+X(I+1)+X(N)
      G(I)=G(I)+4.0D 0*A**3
      G(I+1)=G(I+1)+4.0D 0*A**3
      G(N)=G(N)+4.0D 0*A**3
  451 CONTINUE
      RETURN
  460 A=1.0D 0
      B=0.0D 0
      C=0.0D 0
      D=0.0D 0
      U=EXP(X(N))
      V=EXP(X(N-1))
      DO 461 J=1,N
      IF (J.LE.N-2) THEN
      B=B+(X(J)+2.0D 0*X(J+1)+1.0D 1*X(J+2)-1.0D 0)**2
      C=C+(2.0D 0*X(J)+X(J+1)-3.0D 0)**2
      ENDIF
      D=D+X(J)**2-DBLE(N)
  461 CONTINUE
      DO 462 J=1,N
      IF (J.LE.N/2) G(J)=G(J)+2.0D 0*(X(J)-1.0D 0)
      IF (J.LE.N-2) THEN
      P=A*(U+C)*(X(J)+2.0D 0*X(J+1)+1.0D 1*X(J+2)-1.0D 0)
      Q=A*(V+B)*(2.0D 0*X(J)+X(J+1)-3.0D 0)
      G(J)=G(J)+2.0D 0*P+4.0D 0*Q
      G(J+1)=G(J+1)+4.0D 0*P+2.0D 0*Q
      G(J+2)=G(J+2)+2.0D 1*P
      ENDIF
      G(J)=G(J)+4.0D 0*D*X(J)
  462 CONTINUE
      G(N-1)=G(N-1)+A*V*C
      G(N)=G(N)+A*U*B
      RETURN
  470 DO 471 J=1,N-3,4
      A=X(J)+1.0D 1*X(J+1)
      B=X(J+2)-X(J+3)
      C=X(J+1)-2.0D 0*X(J+2)
      D=X(J)-X(J+3)
      G(J)=G(J)+2.0D 0*A+4.0D 1*D**3
      G(J+1)=G(J+1)+2.0D 1*A+4.0D 0*C**3
      G(J+2)=G(J+2)-8.0D 0*C**3+1.0D 1*B
      G(J+3)=G(J+3)-4.0D 1*D**3-1.0D 1*B
  471 CONTINUE
      RETURN
  480 DO 483 I=1,N
      P=RPAR(I)
      A=(2.0D 0+5.0D 0*(P*X(I))**2)*P*X(I)+1.0D 0
      DO 481 J=MAX(1,I-5),MIN(N,I+1)
      IF (J.NE.I) THEN
      Q=RPAR(J)
      A=A-Q*X(J)*(1.0D 0+Q*X(J))
      ENDIF
  481 CONTINUE
      G(I)=G(I)+2.0D 0*A*P*(2.0D 0+1.5D 1*(P*X(I))**2)
      DO 482 J=MAX(1,I-5),MIN(N,I+1)
      IF (J.NE.I) THEN
      Q=RPAR(J)
      G(J)=G(J)-2.0D 0*A*Q*(1.0D 0+2.0D 0*Q*X(J))
      ENDIF
  482 CONTINUE
  483 CONTINUE
      RETURN
  490 DO 491 I=1,N-2
      A=X(I)-X(I+1)
      B=0.5D 0*(PI*X(I+1)+X(I+2))
      C=COS(B)
      D=X(I)+X(I+2)
      E=D/X(I+1)-2.0D 0
      U=EXP(-E**2)
      V=1.0D 0+A**2
      G(I)=G(I)+2.0D 0*A/V**2+2.0D 0*U*E/X(I+1)
      G(I+1)=G(I+1)-2.0D 0*A/V**2-0.5D 0*PI*C-2.0D 0*U*D*E/X(I+1)**2
      G(I+2)=G(I+2)-0.5D 0*C+2.0D 0*U*E/X(I+1)
  491 CONTINUE
      RETURN
  500 DO 501 I=1,N-1
      P=RPAR(I)
      Q=RPAR(I+1)
      A=(P*X(I))**2-0.5D 0*Q*X(I+1)
      B=SIN(A)
      G(I)=G(I)-2.0D 0*B*P**2*X(I)
      G(I+1)=G(I+1)+0.5D 0*B*Q
  501 CONTINUE
      RETURN
  510 A=X(1)-1.0D 0
      B=X(N)**2-X(1)**2
      G(1)=4.0D 0*A**3-4.0D 0*B*X(1)
      G(N)=4.0D 0*B*X(N)
      DO 511 I=2,N-1
      A=X(I)-X(N)
      B=SIN(A)+X(I)**2-X(1)**2
      G(I)=G(I)+2.0D 0*B*(COS(A)+2.0D 0*X(I))
      G(1)=G(1)-4.0D 0*B*X(1)
      G(N)=G(N)-2.0D 0*B*COS(A)
  511 CONTINUE
      RETURN
  520 DO 521 I=1,N
      I1=MOD(2*I-1,N)+1
      I2=MOD(3*I-1,N)+1
      I3=MOD(5*I-1,N)+1
      I4=MOD(7*I-1,N)+1
      I5=MOD(11*I-1,N)+1
      A=SIN(X(I))+SIN(X(I1))+SIN(X(I2))+SIN(X(I3))+SIN(X(I4))+SIN(X(I5))
      A=A*DBLE(I)
      G(I)=G(I)+A*COS(X(I))
      G(I1)=G(I1)+A*COS(X(I1))
      G(I2)=G(I2)+A*COS(X(I2))
      G(I3)=G(I3)+A*COS(X(I3))
      G(I4)=G(I4)+A*COS(X(I4))
      G(I5)=G(I5)+A*COS(X(I5))
  521 CONTINUE
      RETURN
  530 DO 531 I=1,N
      I1=MOD(2*I-1,N)+1
      I2=MOD(3*I-1,N)+1
      I3=MOD(5*I-1,N)+1
      I4=MOD(7*I-1,N)+1
      I5=MOD(11*I-1,N)+1
      A=5.0D-1*(X(I)**2+X(I1)**2+X(I2)**2+X(I3)**2+X(I4)**2+X(I5)**2)
      A=A*DBLE(I)
      G(I)=G(I)+A*X(I)
      G(I1)=G(I1)+A*X(I1)
      G(I2)=G(I2)+A*X(I2)
      G(I3)=G(I3)+A*X(I3)
      G(I4)=G(I4)+A*X(I4)
      G(I5)=G(I5)+A*X(I5)
  531 CONTINUE
      RETURN
  540 M=(N+2)/3
      DO 542 I=1,M
      J=3*(I-1)+1
      DO 541 K=1,5
      IF (MOD(K,5).EQ.1) THEN
      IF (I.GT.2) THEN
      A=X(J-4)*X(J-1)-RPAR(J-4)*RPAR(J-1)
      G(J-4)=G(J-4)+A*X(J-1)
      G(J-1)=G(J-1)+A*X(J-4)
      ENDIF
      ELSE IF(MOD(K,5).EQ.2) THEN
      IF (I.GT.1) THEN
      A=X(J-3)*X(J-1)+X(J-1)*X(J)-RPAR(J-3)*RPAR(J-1)-RPAR(J-1)*RPAR(J)
      G(J-3)=G(J-3)+A*X(J-1)
      G(J-1)=G(J-1)+A*(X(J-3)+X(J))
      G(J)=G(J)+A*X(J-1)
      ENDIF
      ELSE IF(MOD(K,5).EQ.3) THEN
      IF (I.GT.1) THEN
      A=X(J-2)*X(J-1)-RPAR(J-2)*RPAR(J-1)
      G(J-2)=G(J-2)+A*X(J-1)
      G(J-1)=G(J-1)+A*X(J-2)
      ENDIF
      A=X(J)*X(J)-RPAR(J)*RPAR(J)
      G(J)=G(J)+2.0*A*X(J)
      IF (I.LT.M) THEN
      A=X(J+2)*X(J+1)-RPAR(J+2)*RPAR(J+1)
      G(J+2)=G(J+2)+A*X(J+1)
      G(J+1)=G(J+1)+A*X(J+2)
      ENDIF
      ELSE IF(MOD(K,5).EQ.4) THEN
      IF (I.LT.M) THEN
      A=X(J+3)*X(J+1)+X(J+1)*X(J)-RPAR(J+3)*RPAR(J+1)-RPAR(J+1)*RPAR(J)
      G(J+3)=G(J+3)+A*X(J+1)
      G(J+1)=G(J+1)+A*(X(J+3)+X(J))
      G(J)=G(J)+A*X(J+1)
      ENDIF
      ELSE
      IF (I.LT.M-1) THEN
      A=X(J+4)*X(J+1)-RPAR(J+4)*RPAR(J+1)
      G(J+4)=G(J+4)+A*X(J+1)
      G(J+1)=G(J+1)+A*X(J+4)
      ENDIF
      ENDIF
  541 CONTINUE
  542 CONTINUE
      DO 543 J=1,N
      G(J)=2.0D 0*G(J)
  543 CONTINUE
      RETURN
  550 DO 551 I=2,N,2
      A=X(I)-X(I-1)**2
      G(I-1)=G(I-1)-4.0D 2*A*X(I-1)+2.0D 0*(X(I-1)-1.0D 0)
      G(I)=G(I)+2.0D 2*A
  551 CONTINUE
      RETURN
  560 DO 561 I=1,N-2
      A=1.0D 1/DBLE(N+2)+X(I+2)**2
      B=X(I)-X(I+1)
      C=1.0D-1+X(I+2)**2
      D=-B**2/C
      E=EXP(D)
      G(I)=G(I)+2.0D 0*A*B*E/C
      G(I+1)=G(I+1)-2.0D 0*A*B*E/C
      G(I+2)=G(I+2)+2.0D 0*X(I+2)*(2.0D 0-E*(1.0D 0+A*B*B/(C*C)))
  561 CONTINUE
      RETURN
  570 A=X(1)-1.0D 0
      G(1)=2.0D 0*A
      DO 571 I=1,N-1
      A=X(1)**2-X(I+1)**2
      G(1)=G(1)+4.0D 0*A*X(1)
      G(I+1)=G(I+1)-4.0D 0*A*X(I+1)
  571 CONTINUE
      RETURN
  580 DO 581 J=2,N-2,4
      A=X(J-1)**2-X(J)
      B=X(J-1)-1.0D 0
      C=X(J+1)**2-X(J+2)
      D=X(J)+X(J+2)-2.0D 0
      E=X(J)-X(J+2)
      U=X(J+1)-1.0D 0
      G(J-1)=G(J-1)+4.0D 2*X(J-1)*A+2.0D 0*B
      G(J)=G(J)-2.0D 2*A+2.0D 1*D+0.2D 0*E
      G(J+1)=G(J+1)+3.6D 2*X(J+1)*C+2.0D 0*U
      G(J+2)=G(J+2)-1.8D 2*C+2.0D 1*D-0.2D 0*E
  581 CONTINUE
      RETURN
      END
* SUBROUTINE TFBU11                ALL SYSTEMS                10/12/01
C PORTABILITY : ALL SYSTEMS
C 10/12/01 LU : ORIGINAL VERSION
*
* PURPOSE :
*  VALUES AND GRADIENTS OF MODEL FUNCTIONS FOR UNCONSTRAINED
*  MINIMIZATION. UNIVERSAL VERSION.
*
* PARAMETERS :
*  II  N  NUMBER OF VARIABLES.
*  RI  X(N)  VECTOR OF VARIABLES.
*  RO  F  VALUE OF THE MODEL FUNCTION.
*  RI  G(N)  GRADIENG OF THE MODEL FUNCTION.
*  II  NEXT  NUMBER OF THE TEST PROBLEM.
*
      SUBROUTINE TFBU11(N,X,F,G,NEXT)
      INTEGER N,NEXT
      REAL*8 X(N),G(N),F
      INTEGER I,I1,I2,I3,I4,I5,J,K,L,M
      REAL*8 A,B,C,D,E,P,Q,U,V,H,PI
      REAL*8 RPAR(10000)
      INTEGER IPAR(10),MM
      COMMON /EMPR11/ RPAR,IPAR,MM
      PI=3.14159265358979323846D 0
      F=0.0D 0
      CALL UXVSET(N,0.0D 0,G)
      GO TO (10,20,30,40,50,60,70,80,90,100,110,110,110,110,110,110,
     &  110,110,110,110,110,110,230,240,250,260,270,280,290,300,310,
     &  320,330,340,350,360,370,380,390,400,410,420,430,440,450,460,
     &  470,480,490,500,510,520,530,540,550,560,570,580),NEXT
   10 DO 11 I=1,N-1
      A=X(I)**2+X(N)**2
      F=F+A**2-4.0D 0*X(I)+3.0D 0
      G(I)=4.0D 0*A*X(I)-4.0D 0
      G(N)=G(N)+4.0D 0*A*X(N)
   11 CONTINUE
      RETURN
   20 DO 21 I=1,N-4
      A=3.0D 0-4.0D 0*X(I)
      B=X(I)**2+2.0D 0*X(I+1)**2+3.0D0*X(I+2)**2+4.0D 0*X(I+3)**2+
     & 5.0D 0*X(N)**2
      F=F+A**2+B**2
      G(I)=G(I)+4.0D 0*B*X(I)-8.0D 0*A
      G(I+1)=G(I+1)+8.0D 0*B*X(I+1)
      G(I+2)=G(I+2)+1.2D 1*B*X(I+2)
      G(I+3)=G(I+3)+1.6D 1*B*X(I+3)
      G(N)=G(N)+2.0D 1*B*X(N)
   21 CONTINUE
      RETURN
   30 P=7.0D 0/3.0D 0
      K=N/2
      DO 31 J=1,N
      A=(3.0D 0-2.0D 0*X(J))*X(J)+1.0D 0
      IF (J.GT.1) A=A-X(J-1)
      IF (J.LT.N) A=A-2.0D 0*X(J+1)
      F=F+ABS(A)**P
      B=P*ABS(A)**(P-1.0D 0)*SIGN(1.0D 0,A)
      G(J)=G(J)+B*(3.0D 0-4.0D 0*X(J))
      IF (J.GT.1) G(J-1)=G(J-1)-B
      IF (J.LT.N) G(J+1)=G(J+1)-2.0D 0*B
      IF (J.LE.K) THEN
      A=X(J)+X(J+K)
      F=F+ABS(A)**P
      B=P*ABS(A)**(P-1.0D 0)*SIGN(1.0D 0,A)
      G(J)=G(J)+B
      G(J+K)=G(J+K)+B
      ENDIF
   31 CONTINUE
      RETURN
   40 DO 43 I=1,N
      A=(2.0D 0+5.0D 0*X(I)**2)*X(I)+1.0D 0
      DO 41 J=MAX(1,I-5),MIN(N,I+1)
      IF (J.NE.I) A=A-X(J)*(1.0D 0+X(J))
   41 CONTINUE
      F=F+A*A
      G(I)=G(I)+2.0D 0*A*(2.0D 0+1.5D 1*X(I)**2)
      DO 42 J=MAX(1,I-5),MIN(N,I+1)
      IF (J.NE.I) G(J)=G(J)-2.0D 0*A*(1.0D 0+2.0D 0*X(J))
   42 CONTINUE
   43 CONTINUE
      RETURN
   50 F=1.0D 0
      DO 51 J=2,N-2,2
      A=X(J-1)**2-X(J)
      B=X(J-1)-1.0D 0
      C=X(J+1)**2-X(J+2)
      D=X(J+1)-1.0D 0
      U=X(J)+X(J+2)-2.0D 0
      V=X(J)-X(J+2)
      F=F+1.0D 2*A**2+B**2+9.0D 1*C**2+D**2+1.0D 1*U**2+0.1D 0*V**2
      G(J-1)=G(J-1)+4.0D 2*X(J-1)*A+2.0D 0*B
      G(J)=G(J)-2.0D 2*A+2.0D 1*U+0.2D 0*V
      G(J+1)=G(J+1)+3.6D 2*X(J+1)*C+2.0D 0*D
      G(J+2)=G(J+2)-1.8D 2*C+2.0D 1*U-0.2D 0*V
   51 CONTINUE
      RETURN
   60 DO 61 I=1,N-1
      A=X(I)**2-0.5D 0*X(I+1)
      F=F+COS(A)
      B=SIN(A)
      G(I)=G(I)-2.0D 0*B*X(I)
      G(I+1)=G(I+1)+0.5D 0*B
   61 CONTINUE
      RETURN
   70 DO 71 J=2,N-2,2
      A=EXP(X(J-1))
      B=A-X(J)
      D=X(J)-X(J+1)
      P=X(J+1)-X(J+2)
      C=COS(P)
      Q=SIN(P)/C
      U=X(J-1)
      V=X(J+2)-1.0D 0
      F=F+B**4+1.0D 2*D**6+(Q+P)**4+U**8+V**2
      B=4.0D 0*B**3
      D=6.0D 2*D**5
      E=4.0D 0*(Q+P)**3
      Q=E*(1.0D 0+1.0D 0/C**2)
      G(J-1)=G(J-1)+A*B+8.0D 0*U**7
      G(J)=G(J)+D-B
      G(J+1)=G(J+1)+Q-D
      G(J+2)=G(J+2)+2.0D 0*V-Q
   71 CONTINUE
      RETURN
   80 K=10
      GO TO 101
   90 K=20
      GO TO 101
  100 K=30
  101 DO 104 I=1,N
      A=0.0D 0
      DO 102 J=I,MIN(I+K,N)
      A=A+X(J)
  102 CONTINUE
      F=F+A*(A*(A**2-2.0D 1)-1.0D-1)
      B=4.0D 0*A*(A**2-1.0D 1)-1.0D-1
      DO 103 J=I,MIN(I+K,N)
      G(J)=G(J)+B
  103 CONTINUE
  104 CONTINUE
      RETURN
  110 M=N/3
      F=1.0D 0
      DO 111 I=1,N
      A=RPAR(1)*(DBLE(I)/DBLE(N))**IPAR(1)
      F=F+A*X(I)**2
      G(I)=G(I)+2.0D 0*A*X(I)
  111 CONTINUE
      DO 112 I=1,N-1
      A=RPAR(2)*(DBLE(I)/DBLE(N))**IPAR(2)
      B=X(I+1)+X(I+1)**2
      F=F+A*X(I)**2*B**2
      G(I)=G(I)+2.0D 0*A*B**2*X(I)
      G(I+1)=G(I+1)+A*B*X(I)**2*(4.0D 0*X(I+1)+2.0D 0)
  112 CONTINUE
      DO 113 I=1,2*M
      A=RPAR(3)*(DBLE(I)/DBLE(N))**IPAR(3)
      F=F+A*X(I)**2*X(I+M)**4
      G(I)=G(I)+2.0D 0*A*X(I)*X(I+M)**4
      G(I+M)=G(I+M)+4.0D 0*A*X(I)**2*X(I+M)**3
  113 CONTINUE
      DO 114 I=1,M
      A=RPAR(4)*(DBLE(I)/DBLE(N))**IPAR(4)
      F=F+A*X(I)*X(I+2*M)
      G(I)=G(I)+A*X(I+2*M)
      G(I+2*M)=G(I+2*M)+A*X(I)
  114 CONTINUE
      RETURN
  230 DO 231 I=1,N
      F=F+(X(I)-DBLE(I))**4
      G(I)=G(I)+4.0D 0*(X(I)-DBLE(I))**3
  231 CONTINUE
      RETURN
  240 F=1.6D 1
      DO 241 I=1,N-1
      A=X(I)*X(I+1)-2.0D0*X(I+1)
      F=F+(X(I)-2.0D 0)**4+A**2+(X(I+1)+1.0D 0)**2
      G(I)=G(I)+4.0D 0*(X(I)-2.0D 0)**3+2.0D 0*A*X(I+1)
      G(I+1)=G(I+1)+2.0D 0*A*(X(I)-2.0D 0)+2.0D 0*(X(I+1)+1.0D 0)
  241 CONTINUE
      RETURN
  250 DO 251 I=1,N-1
      A=X(1)+X(I)**2-1.0D 0
      F=F+SIN(A)
      B=COS(A)
      G(1)=G(1)+B
      G(I)=G(I)+2.0D 0*X(I)*B
  251 CONTINUE
      F=F+0.5D0*SIN(X(N)**2)
      G(N)=G(N)+COS(X(N)**2)*X(N)
      RETURN
  260 DO 261 I=1,N-1
      A=X(I)**2+X(I+1)**2
      F=F+A**2+3.0D 0-4.0D 0*X(I)
      G(I)=G(I)+4.0D 0*A*X(I)-4.0D 0
      G(I+1)=G(I+1)+4.0D 0*A*X(I+1)
  261 CONTINUE
      RETURN
  270 DO 271 I=2,N
      A=1.6D 1*(1.5D 0+SIN(DBLE(I)))**2
      B=X(I-1)-X(I)**2
      F=F+A*B**2+(X(I)-1.0D 0)**2
      G(I)=G(I)-4.0D 0*A*B*X(I)+2.0D 0*(X(I)-1.0D0)
      G(I-1)=G(I-1)+2.0D 0*A*B
  271 CONTINUE
      RETURN
  280 DO 281 I=2,N
      A=1.6D 1*(1.5D 0+SIN(DBLE(I)))**2
      B=X(I-1)-A*X(I)**2
      F=F+B**2+(X(I)-1.0D 0)**2
      G(I)=G(I)-4.0D 0*A*B*X(I)+2.0D 0*(X(I)-1.0D0)
      G(I-1)=G(I-1)+2.0D 0*B
  281 CONTINUE
      RETURN
  290 F=(X(1)-1.0D 0)**2
      G(1)=2.0D 0*(X(1)-1.0D 0)
      DO 291 I=2,N
      A=X(I)-X(I-1)**2
      F=F+1.0D 2*A**2
      G(I)=G(I)+2.0D 2*A
      G(I-1)=G(I-1)-4.0D 2*A*X(I-1)
  291 CONTINUE
      RETURN
  300 H=1.0D 0/DBLE(N+1)**2
      P=1.0D 0/RPAR(2)
      F=0.5D 0*P*X(1)**2+0.5D 0*P*X(N)**2
      G(1)=P*X(1)
      G(N)=P*X(N)
      DO 301 I=1,N-1
      A=X(I)-X(I+1)
      F=F+0.5D 0*P*A**2
      G(I)=G(I)+P*A
      G(I+1)=G(I+1)-P*A
  301 CONTINUE
      A=1.0D 0+2.0D 0/H
      DO 302 I=1,N
      F=F-P*(A*1.0D 2*SIN(X(I)/1.0D 2)+RPAR(1)*COS(X(I))/H)
      G(I)=G(I)-P*(A*COS(X(I)/1.0D 2)-RPAR(1)*SIN(X(I))/H)
  302 CONTINUE
      RETURN
  310 H=1.0D 0/DBLE(N+1)**2
      F=0.5D 0*X(1)**2+0.5D 0*X(N)**2
      G(1)=X(1)
      G(N)=X(N)
      DO 311 I=1,N-1
      A=X(I)-X(I+1)
      F=F+0.5D 0*A**2
      G(I)=G(I)+A
      G(I+1)=G(I+1)-A
  311 CONTINUE
      A=2.0D 0*H
      DO 312 I=1,N-1
      F=F-A*X(I)-RPAR(1)*COS(X(I))*H
      G(I)=G(I)-A+RPAR(1)*SIN(X(I))*H
  312 CONTINUE
      A=1.0D 0+2.0D 0*H
      F=F-A*X(N)-RPAR(1)*COS(X(N))*H
      G(N)=G(N)-A+RPAR(1)*SIN(X(I))*H
      RETURN
  320 DO 321 I=1,N-1
      A=X(I)*(X(I)+1.0D 0)-X(I+1)-1.0D 0
      F=F+1.0D 2*A**2
      G(I)=G(I)+2.0D 2*A*(2.0D 0*X(I)+1.0D 0)
      G(I+1)=G(I+1)-2.0D 2*A
  321 CONTINUE
      RETURN
  330 P=DBLE(MM-1)**2
      L=0
      DO 332 I=1,MM-1
      DO 331 J=1,MM-1
      A=X(L+J)-X(L+MM+J+1)
      B=X(L+MM+J)-X(L+J+1)
      C=0.5D 0*P*(A**2+B**2)+1.0D 0
      F=F+SQRT(C)/P
      D=0.5D 0/SQRT(C)
      G(L+J)=G(L+J)+D*A
      G(L+MM+J+1)=G(L+MM+J+1)-D*A
      G(L+MM+J)=G(L+MM+J)+D*B
      G(L+J+1)=G(L+J+1)-D*B
  331 CONTINUE
      L=L+MM
  332 CONTINUE
      L=MM*(MM-1)/2
      F=F+X(L)**2/DBLE(MM**2)
      G(L)=G(L)+2.0D 0*X(L)/DBLE(MM**2)
      RETURN
  340 DO 341 I=1,N-1
      A=X(I)+((5.0D 0-X(I+1))*X(I+1)-2.0D 0)*X(I+1)-1.3D 1
      F=F+A**2
      G(I)=G(I)+A
      G(I+1)=G(I+1)+(1.0D 1*X(I+1)-3.0D 0*X(I+1)**2-2.0D 0)*A
      A=X(I)+((X(I+1)+1.0D 0)*X(I+1)-1.4D 1)*X(I+1)-2.9D 1
      F=F+A**2
      G(I)=G(I)+A
      G(I+1)=G(I+1)+(3.0D 0*X(I+1)**2+2.0D 0*X(I+1)-1.4D 1)*A
  341 CONTINUE
      RETURN
  350 P=RPAR(1)
      DO 351 I=1,N-1
      A=SIN(P*X(I))
      B=SIN(P*X(I+1))
      F=F+A**2*B**2+5.0D-2*(X(I)**2+X(I+1)**2)
      G(I)=G(I)+2.0D 0*P*A*B**2*COS(P*X(I))+1.0D-1*X(I)
      G(I+1)=G(I+1)+2.0D 0*P*A**2*B*COS(P*X(I+1))+1.0D-1*X(I+1)
  351 CONTINUE
      RETURN
  360 F=1.0D 0
      DO 361 I=2,N
      A=X(I)-X(I-1)**2
      F=F+1.0D 2*A**2+(X(I)-1.0D 0)**2
      G(I)=G(I)+2.0D 2*A+2.0D 0*(X(I)-1.0D 0)
      G(I-1)=G(I-1)-4.0D 2*A*X(I-1)
  361 CONTINUE
      RETURN
  370 DO 371 I=1,N
      F=F+1.0D 2*SIN(X(I)/1.0D 2)
      G(I)=G(I)+COS(X(I)/1.0D 2)
  371 CONTINUE
      DO 372 I=2,N-1
      A=2.0D 0*X(I)-X(N)-X(1)
      F=F+RPAR(1)*COS(A)
      B=RPAR(1)*SIN(A)
      G(I)=G(I)-2.0D 0*B
      G(1)=G(1)+B
      G(N)=G(N)+B
  372 CONTINUE
      RETURN
  380 DO 381 I=1,N
      A=X(I)**2-X(1)
      F=F+4.0D 0*A**2+(X(I)-1.0D 0)**2
      G(I)=G(I)+1.6D 1*A*X(I)+2.0D 0*(X(I)-1.0D 0)
      G(1)=G(1)-8.0D 0*A
  381 CONTINUE
      RETURN
  390 P=1.0D 0/DBLE(N+1)
      Q=0.5D 0*P**2
      DO 391 I=1,N
      A=2.0D 0*X(I)+Q*(X(I)+DBLE(I)*P+1.0D 0)**3
      IF (I.GT.1) A=A-X(I-1)
      IF (I.LT.N) A=A-X(I+1)
      F=F+A**2
      G(I)=G(I)+A*(4.0D 0+6.0D 0*Q*(X(I)+DBLE(I)*P+1.0D 0)**2)
      IF(I.GT.1) G(I-1)=G(I-1)-2.0D 0*A
      IF(I.LT.N) G(I+1)=G(I+1)-2.0D 0*A
  391 CONTINUE
      RETURN
  400 L=IPAR(1)
      M=IPAR(2)
      F=2.0D 0
      DO 403 I=1,N-L-M
      C=1.0D 1/DBLE(I)
      D=0.0D 0
      DO 401 J=1,L
      A=X(I+J-1)
      B=1.0D 0+A*A
      D=D+A/B
      F=F+RPAR(2)*A
      G(I+J-1)=G(I+J-1)+RPAR(2)
  401 CONTINUE
      F=F+C*D*D
      DO 402 J=1,L
      A=X(I+J-1)
      B=1.0D 0+A*A
      G(I+J-1)=G(I+J-1)+2.0D 0*C*D*(1-A*A)/B**2
  402 CONTINUE
  403 CONTINUE
      DO 404 I=1,N-M
      F=F+X(I)**4+2.0D 0
      G(I)=G(I)+4.0D 0*X(I)**3
  404 CONTINUE
      DO 405 I=1,M
      F=F+RPAR(1)*(X(I)*X(I+M)*X(I+N-M)+2.0D 0*X(I+N-M)**2)
      G(I)=G(I)+RPAR(1)*X(I+M)*X(I+N-M)
      G(I+M)=G(I+M)+RPAR(1)*X(I)*X(I+N-M)
      G(I+N-M)=G(I+N-M)+RPAR(1)*(X(I)*X(I+M)+4.0D 0*X(I+N-M))
  405 CONTINUE
      RETURN
  410 L=IPAR(1)
      DO 413 I=1,N-L+1
      C=1.0D 1/DBLE(I)
      D=0.0D 0
      DO 411 J=1,L
      A=X(I+J-1)
      B=1.0D 0+A*A
      D=D+A/B
      F=F+RPAR(2)*A
      G(I+J-1)=G(I+J-1)+RPAR(2)
  411 CONTINUE
      F=F+C*D*D
      DO 412 J=1,L
      A=X(I+J-1)
      B=1.0D 0+A*A
      G(I+J-1)=G(I+J-1)+2.0D 0*C*D*(1-A*A)/B**2
  412 CONTINUE
  413 CONTINUE
      DO 414 I=1,N
      F=F+RPAR(1)*X(I)**4+2.0D 0
      G(I)=G(I)+4.0D 0*RPAR(1)*X(I)**3
  414 CONTINUE
      RETURN
  420 DO 421 I=1,N
      K=MOD(2*I-1,N)
      L=MOD(3*I-1,N)
      A=X(I)+X(K+1)+X(L+1)
      F=F+A**2+4.0D 0*COS(A)
      B=SIN(A)
      G(I)=G(I)+2.0D 0*A-4.0D 0*B
      G(K+1)=G(K+1)+2.0D 0*A-4.0D 0*B
      G(L+1)=G(L+1)+2.0D 0*A-4.0D 0*B
  421 CONTINUE
      RETURN
  430 DO 431 I=1,N
      K=MOD(3*I-2,N)
      L=MOD(7*I-3,N)
      A=X(I)+X(K+1)+X(L+1)
      F=F+A**2+4.0D 0*COS(A)
      B=SIN(A)
      G(I)=G(I)+2.0D 0*A-4.0D 0*B
      G(K+1)=G(K+1)+2.0D 0*A-4.0D 0*B
      G(L+1)=G(L+1)+2.0D 0*A-4.0D 0*B
  431 CONTINUE
      RETURN
  440 F=(X(1)-1.0D 0)**2
      G(1)=2.0D 0*(X(1)-1.0D 0)
      DO 441 I=2,N
      A=X(1)-X(I-1)**2
      F=F+1.0D 2*A**2
      G(1)=G(1)+2.0D 2*A
      G(I-1)=G(I-1)-4.0D 2*A*X(I-1)
  441 CONTINUE
      RETURN
  450 A=X(1)-X(2)
      B=X(N-1)-X(N)
      F=A**2+B**2
      G(1)=2.0D 0*A
      G(2)=-2.0D 0*A
      G(N-1)=2.0D 0*B
      G(N)=-2.0D 0*B
      DO 451 I=1,N-2
      A=X(I)+X(I+1)+X(N)
      F=F+A**4
      G(I)=G(I)+4.0D 0*A**3
      G(I+1)=G(I+1)+4.0D 0*A**3
      G(N)=G(N)+4.0D 0*A**3
  451 CONTINUE
      RETURN
  460 A=1.0D 0
      B=0.0D 0
      C=0.0D 0
      D=0.0D 0
      F=0.0D 0
      U=EXP(X(N))
      V=EXP(X(N-1))
      DO 461 J=1,N
      IF (J.LE.N/2) F=F+(X(J)-1.0D 0)**2
      IF (J.LE.N-2) THEN
      B=B+(X(J)+2.0D 0*X(J+1)+1.0D 1*X(J+2)-1.0D 0)**2
      C=C+(2.0D 0*X(J)+X(J+1)-3.0D 0)**2
      ENDIF
      D=D+X(J)**2-DBLE(N)
  461 CONTINUE
      F=F+A*(1.0D 0+U*B+B*C+V*C)+D**2
      DO 462 J=1,N
      IF (J.LE.N/2) G(J)=G(J)+2.0D 0*(X(J)-1.0D 0)
      IF (J.LE.N-2) THEN
      P=A*(U+C)*(X(J)+2.0D 0*X(J+1)+1.0D 1*X(J+2)-1.0D 0)
      Q=A*(V+B)*(2.0D 0*X(J)+X(J+1)-3.0D 0)
      G(J)=G(J)+2.0D 0*P+4.0D 0*Q
      G(J+1)=G(J+1)+4.0D 0*P+2.0D 0*Q
      G(J+2)=G(J+2)+2.0D 1*P
      ENDIF
      G(J)=G(J)+4.0D 0*D*X(J)
  462 CONTINUE
      G(N-1)=G(N-1)+A*V*C
      G(N)=G(N)+A*U*B
      RETURN
  470 DO 471 J=1,N-3,4
      A=X(J)+1.0D 1*X(J+1)
      B=X(J+2)-X(J+3)
      C=X(J+1)-2.0D 0*X(J+2)
      D=X(J)-X(J+3)
      F=F+A**2+5.0D 0*B**2+C**4+1.0D 1*D**4
      G(J)=G(J)+2.0D 0*A+4.0D 1*D**3
      G(J+1)=G(J+1)+2.0D 1*A+4.0D 0*C**3
      G(J+2)=G(J+2)-8.0D 0*C**3+1.0D 1*B
      G(J+3)=G(J+3)-4.0D 1*D**3-1.0D 1*B
  471 CONTINUE
      RETURN
  480 DO 483 I=1,N
      P=RPAR(I)
      A=(2.0D 0+5.0D 0*(P*X(I))**2)*P*X(I)+1.0D 0
      DO 481 J=MAX(1,I-5),MIN(N,I+1)
      IF (J.NE.I) THEN
      Q=RPAR(J)
      A=A-Q*X(J)*(1.0D 0+Q*X(J))
      ENDIF
  481 CONTINUE
      F=F+A*A
      G(I)=G(I)+2.0D 0*A*P*(2.0D 0+1.5D 1*(P*X(I))**2)
      DO 482 J=MAX(1,I-5),MIN(N,I+1)
      IF (J.NE.I) THEN
      Q=RPAR(J)
      G(J)=G(J)-2.0D 0*A*Q*(1.0D 0+2.0D 0*Q*X(J))
      ENDIF
  482 CONTINUE
  483 CONTINUE
      RETURN
  490 DO 491 I=1,N-2
      A=X(I)-X(I+1)
      B=0.5D 0*(PI*X(I+1)+X(I+2))
      C=COS(B)
      D=X(I)+X(I+2)
      E=D/X(I+1)-2.0D 0
      U=EXP(-E**2)
      V=1.0D 0+A**2
      F=F-1.0D 0/V-SIN(B)-U
      G(I)=G(I)+2.0D 0*A/V**2+2.0D 0*U*E/X(I+1)
      G(I+1)=G(I+1)-2.0D 0*A/V**2-0.5D 0*PI*C-2.0D 0*U*D*E/X(I+1)**2
      G(I+2)=G(I+2)-0.5D 0*C+2.0D 0*U*E/X(I+1)
  491 CONTINUE
      RETURN
  500 DO 501 I=1,N-1
      P=RPAR(I)
      Q=RPAR(I+1)
      A=(P*X(I))**2-0.5D 0*Q*X(I+1)
      F=F+COS(A)
      B=SIN(A)
      G(I)=G(I)-2.0D 0*B*P**2*X(I)
      G(I+1)=G(I+1)+0.5D 0*B*Q
  501 CONTINUE
      RETURN
  510 A=X(1)-1.0D 0
      B=X(N)**2-X(1)**2
      F=A**4+B**2
      G(1)=4.0D 0*A**3-4.0D 0*B*X(1)
      G(N)=4.0D 0*B*X(N)
      DO 511 I=2,N-1
      A=X(I)-X(N)
      B=SIN(A)+X(I)**2-X(1)**2
      F=F+B**2
      G(I)=G(I)+2.0D 0*B*(COS(A)+2.0D 0*X(I))
      G(1)=G(1)-4.0D 0*B*X(1)
      G(N)=G(N)-2.0D 0*B*COS(A)
  511 CONTINUE
      RETURN
  520 DO 521 I=1,N
      I1=MOD(2*I-1,N)+1
      I2=MOD(3*I-1,N)+1
      I3=MOD(5*I-1,N)+1
      I4=MOD(7*I-1,N)+1
      I5=MOD(11*I-1,N)+1
      A=SIN(X(I))+SIN(X(I1))+SIN(X(I2))+SIN(X(I3))+SIN(X(I4))+SIN(X(I5))
      F=F+DBLE(I)*A*A
      A=A*DBLE(I)
      G(I)=G(I)+A*COS(X(I))
      G(I1)=G(I1)+A*COS(X(I1))
      G(I2)=G(I2)+A*COS(X(I2))
      G(I3)=G(I3)+A*COS(X(I3))
      G(I4)=G(I4)+A*COS(X(I4))
      G(I5)=G(I5)+A*COS(X(I5))
  521 CONTINUE
      F=5.0D-1*F
      RETURN
  530 DO 531 I=1,N
      I1=MOD(2*I-1,N)+1
      I2=MOD(3*I-1,N)+1
      I3=MOD(5*I-1,N)+1
      I4=MOD(7*I-1,N)+1
      I5=MOD(11*I-1,N)+1
      A=5.0D-1*(X(I)**2+X(I1)**2+X(I2)**2+X(I3)**2+X(I4)**2+X(I5)**2)
      F=F+DBLE(I)*A*A
      A=A*DBLE(I)
      G(I)=G(I)+A*X(I)
      G(I1)=G(I1)+A*X(I1)
      G(I2)=G(I2)+A*X(I2)
      G(I3)=G(I3)+A*X(I3)
      G(I4)=G(I4)+A*X(I4)
      G(I5)=G(I5)+A*X(I5)
  531 CONTINUE
      F=5.0D-1*F
      RETURN
  540 M=(N+2)/3
      DO 542 I=1,M
      J=3*(I-1)+1
      DO 541 K=1,5
      IF (MOD(K,5).EQ.1) THEN
      IF (I.GT.2) THEN
      A=X(J-4)*X(J-1)-RPAR(J-4)*RPAR(J-1)
      F=F+A*A
      G(J-4)=G(J-4)+A*X(J-1)
      G(J-1)=G(J-1)+A*X(J-4)
      ENDIF
      ELSE IF(MOD(K,5).EQ.2) THEN
      IF (I.GT.1) THEN
      A=X(J-3)*X(J-1)+X(J-1)*X(J)-RPAR(J-3)*RPAR(J-1)-RPAR(J-1)*RPAR(J)
      F=F+A*A
      G(J-3)=G(J-3)+A*X(J-1)
      G(J-1)=G(J-1)+A*(X(J-3)+X(J))
      G(J)=G(J)+A*X(J-1)
      ENDIF
      ELSE IF(MOD(K,5).EQ.3) THEN
      IF (I.GT.1) THEN
      A=X(J-2)*X(J-1)-RPAR(J-2)*RPAR(J-1)
      F=F+A*A
      G(J-2)=G(J-2)+A*X(J-1)
      G(J-1)=G(J-1)+A*X(J-2)
      ENDIF
      A=X(J)*X(J)-RPAR(J)*RPAR(J)
      F=F+A*A
      G(J)=G(J)+2.0*A*X(J)
      IF (I.LT.M) THEN
      A=X(J+2)*X(J+1)-RPAR(J+2)*RPAR(J+1)
      F=F+A*A
      G(J+2)=G(J+2)+A*X(J+1)
      G(J+1)=G(J+1)+A*X(J+2)
      ENDIF
      ELSE IF(MOD(K,5).EQ.4) THEN
      IF (I.LT.M) THEN
      A=X(J+3)*X(J+1)+X(J+1)*X(J)-RPAR(J+3)*RPAR(J+1)-RPAR(J+1)*RPAR(J)
      F=F+A*A
      G(J+3)=G(J+3)+A*X(J+1)
      G(J+1)=G(J+1)+A*(X(J+3)+X(J))
      G(J)=G(J)+A*X(J+1)
      ENDIF
      ELSE
      IF (I.LT.M-1) THEN
      A=X(J+4)*X(J+1)-RPAR(J+4)*RPAR(J+1)
      F=F+A*A
      G(J+4)=G(J+4)+A*X(J+1)
      G(J+1)=G(J+1)+A*X(J+4)
      ENDIF
      ENDIF
  541 CONTINUE
  542 CONTINUE
      DO 543 J=1,N
      G(J)=2.0D 0*G(J)
  543 CONTINUE
      RETURN
  550 DO 551 I=2,N,2
      A=X(I)-X(I-1)**2
      F=F+1.0D 2*A**2+(X(I-1)-1.0D 0)**2
      G(I-1)=G(I-1)-4.0D 2*A*X(I-1)+2.0D 0*(X(I-1)-1.0D 0)
      G(I)=G(I)+2.0D 2*A
  551 CONTINUE
      RETURN
  560 DO 561 I=1,N-2
      A=1.0D 1/DBLE(N+2)+X(I+2)**2
      B=X(I)-X(I+1)
      C=1.0D-1+X(I+2)**2
      D=-B**2/C
      E=EXP(D)
      F=F+A*(2.0D 0-E)
      G(I)=G(I)+2.0D 0*A*B*E/C
      G(I+1)=G(I+1)-2.0D 0*A*B*E/C
      G(I+2)=G(I+2)+2.0D 0*X(I+2)*(2.0D 0-E*(1.0D 0+A*B*B/(C*C)))
  561 CONTINUE
      RETURN
  570 A=X(1)-1.0D 0
      F=A**2
      G(1)=2.0D 0*A
      DO 571 I=1,N-1
      A=X(1)**2-X(I+1)**2
      F=F+A**2
      G(1)=G(1)+4.0D 0*A*X(1)
      G(I+1)=G(I+1)-4.0D 0*A*X(I+1)
  571 CONTINUE
      RETURN
  580 DO 581 J=2,N-2,4
      A=X(J-1)**2-X(J)
      B=X(J-1)-1.0D 0
      C=X(J+1)**2-X(J+2)
      D=X(J)+X(J+2)-2.0D 0
      E=X(J)-X(J+2)
      U=X(J+1)-1.0D 0
      F=F+1.0D 2*A**2+B**2+9.0D 1*C**2+1.0D 1*D**2+1.0D-1*E**2+U**2
      G(J-1)=G(J-1)+4.0D 2*X(J-1)*A+2.0D 0*B
      G(J)=G(J)-2.0D 2*A+2.0D 1*D+0.2D 0*E
      G(J+1)=G(J+1)+3.6D 2*X(J+1)*C+2.0D 0*U
      G(J+2)=G(J+2)-1.8D 2*C+2.0D 1*D-0.2D 0*E
  581 CONTINUE
      RETURN
      END
