PROGRAM MAIN
      INTEGER N, NEXT, IERR
      PARAMETER (N=10)
      REAL*8 X(N), FMIN, XMAX
      
C     设置测试参数
      NEXT = 1
      
C     调用子程序
      CALL TIUD11(N, X, FMIN, XMAX, NEXT, IERR)
      
C     输出结果
      WRITE(*,*) 'FMIN = ', FMIN
      WRITE(*,*) 'XMAX = ', XMAX
      WRITE(*,*) 'IERR = ', IERR
      WRITE(*,*) 'X(1) = ', X(1)
      
      END