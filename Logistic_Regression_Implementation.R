setwd("C:/Users/z00261uy/Desktop/NN_test")
data <- read.table('data_banknote_authentication.txt',sep=',')
ndata <- nrow(data)
smp_size <- floor(0.75 * ndata)
tr.idx <- sample(1:ndata, size = smp_size)
X <- as.matrix(data[tr.idx,1:4])
y <- as.matrix(data[tr.idx,5])
m <- nrow(X)

Xtest <- as.matrix(data[-tr.idx,1:4])
ytest <- as.matrix(data[-tr.idx,5])

sigmoid <- function(x){
  return(1/(1+exp(-x)))
}

calculate_cost <- function(y,a){
  -(y*log(a)+((1-y)*log(1-a)))
}

calc_dz <- function(y,a){
  ((-y/a)+((1-y)/(1-a)))*(a*(1-a))
}

learning_rate <- 0.001

w1 = 0; w2 = 0; w3 = 0 ; w4 = 0;b = 0; Jold = 10^20; Jnew <- 10^10

tolerance <- 10^(-5)
difference <- 10^9
i <- 1
while(difference >= tolerance){
  Z <-  X %*% as.matrix(c(w1,w2,w3,w4))
  A <- sigmoid(Z)
  Jold <- Jnew
  Jnew <- mean(calculate_cost(y,A))
  difference <- abs(Jold-Jnew)
  cat('Iteration',i,'\n')
  cat('value of J is:  ',Jnew,'\n')
  dz <- calc_dz(y,A)
  x1dz <- X[,1]* dz
  x2dz <- X[,2]*dz
  x3dz <- X[,3]* dz
  x4dz <- X[,4]*dz
  dw1 <- mean(x1dz)
  dw2 <- mean(x2dz)
  dw3 <- mean(x3dz)
  dw4 <- mean(x4dz)
  db <- mean(dz)
  w1 <- w1 - (learning_rate*dw1)
  w2 <- w2 - (learning_rate*dw2)
  w3 <- w3 - (learning_rate*dw3)
  w2 <- w4 - (learning_rate*dw4)
  b <- b - (learning_rate*db)
  i <- i+1
}
w <- c(w1,w2,w3,w4)
zhat <- (Xtest %*% w)+b
yprob <- sigmoid(zhat)
yhat <- as.numeric(yprob > 0.5)
table(yhat,ytest)
