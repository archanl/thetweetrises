# The first column is the number of input tweets
# the second column is the percent correct
base_directory = "C:\\Users\\Louis\\thetweetrises\\NLP\\Plots\\"
naive_bayes = as.matrix(read.csv(paste(base_directory, "naive_bayes_file_1.txt", sep=""), header=FALSE))
max_ent = as.matrix(read.csv(paste(base_directory, "max_ent_file_1.txt", sep=""), header=FALSE))
sgd = as.matrix(read.csv(paste(base_directory, "sgd_file_1.txt", sep=""), header=FALSE))
svm = as.matrix(read.csv(paste(base_directory, "svm_file_1.txt", sep=""), header=FALSE))

plot(naive_bayes[,1], naive_bayes[,3], xlab="Number of Trial Tweets", ylab="Accuracy", type="p", col="red", yaxt='n')
par(new=TRUE)
plot(max_ent[,1], max_ent[,3], col="blue", xaxt='n', yaxt='n', ann=FALSE)
par(new=TRUE)
plot(sgd[,1], sgd[,3], col="green", xaxt='n', yaxt='n', ann=FALSE)
par(new=TRUE)
plot(svm[,1], svm[,3], col="purple", xaxt='n', yaxt='n', ann=FALSE)

max_accuracy = max(max(naive_bayes[,3]),max(max_ent[,3]), max(sgd[,3]), max(svm[,3]))
axis(side=2, at=round(seq(0, max_accuracy, by=(max_accuracy / 10)), 2), las=1)

legend("topleft", col=c("red", "blue", "green", "purple"), 
	legend=c("Naive Bayes", "Maximum Entropy", "Stochastic Gradient Descent", "Support Vector Machines"),
	cex=.7, pch=1, pt.cex = 1)	
title("Accuracy by Number of Tweets")

# Plot the time to finish the algorithm

plot(naive_bayes[,1], naive_bayes[,2], xlab="Number of Trial Tweets", ylab="Time (s)", type="p", col="red", yaxt='n')
par(new=TRUE)
plot(max_ent[,1], max_ent[,2], col="blue", xaxt='n', yaxt='n', ann=FALSE)
par(new=TRUE)
plot(sgd[,1], sgd[,2], col="green", xaxt='n', yaxt='n', ann=FALSE)
par(new=TRUE)
plot(svm[,1], svm[,2], col="purple", xaxt='n', yaxt='n', ann=FALSE)

max_time = max(max(naive_bayes[,2]),max(max_ent[,2]), max(sgd[,2]), max(svm[,2]))
axis(side=2, at=seq(0, max_time, by=(max_time / 10)))

legend("topleft", col=c("red", "blue", "green", "purple"), 
       legend=c("Naive Bayes", "Maximum Entropy", "Stochastic Gradient Descent", "Support Vector Machines"),
       cex=.7, pch=1, pt.cex = 1)	
title("Algorithm Run Time by Number of Tweets")

#plot(naive_bayes, xlab="Number of Trial Tweets", ylab="Accuracy", type="p", col="red")
#title("Naive Bayes Over Whole Go Data Set")