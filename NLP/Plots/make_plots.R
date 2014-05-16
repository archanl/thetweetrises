# The first column is the number of input tweets
# the second column is the percent correct
base_directory = "C:\\Users\\Louis\\thetweetrises\\NLP\\Plots\\"
naive_bayes = as.matrix(read.csv(paste(base_directory, "naive_bayes_file_1.txt", sep=""), header=FALSE))
max_ent = as.matrix(read.csv(paste(base_directory, "max_ent_file_1.txt", sep=""), header=FALSE))
sgd = as.matrix(read.csv(paste(base_directory, "sgd_file_1.txt", sep=""), header=FALSE))
svm = as.matrix(read.csv(paste(base_directory, "svm_file_1.txt", sep=""), header=FALSE))

max_accuracy = max(max(naive_bayes[,3]),max(max_ent[,3]), max(sgd[,3]), max(svm[,3]))
min_accuracy = min(min(naive_bayes[,3]), min(max_ent[,3]), min(sgd[,3]), min(svm[,3]))
plot(naive_bayes[,1], naive_bayes[,3], xlab="Number of Trial Tweets", ylab="Accuracy", 
     type="p", col="red", yaxt='n', ylim=c(min_accuracy, max_accuracy))
par(new=TRUE)
points(max_ent[,1], max_ent[,3], col="blue")
par(new=TRUE)
points(sgd[,1], sgd[,3], col="green")
par(new=TRUE)
points(svm[,1], svm[,3], col="purple")

axis(side=2, las=1, ylim=c(0, max_accuracy))

legend("topleft", col=c("red", "blue", "green", "purple"), 
	legend=c("Naive Bayes", "Maximum Entropy", "Stochastic Gradient Descent", "Support Vector Machines"),
	cex=.7, pch=1, pt.cex = 1)	
title("Accuracy by Number of Tweets")

# Plot the time to finish the algorithm

max_time = max(max(naive_bayes[,2]),max(max_ent[,2]), max(sgd[,2]), max(svm[,2]))
plot(naive_bayes[,1], naive_bayes[,2], xlab="Number of Trial Tweets", 
     ylab="Time (s)", type="p", col="red", yaxt='n',
     ylim=c(0, max_time))
#par(new=TRUE)
#plot(max_ent[,1], max_ent[,2], col="blue", xaxt='n', yaxt='n', ann=FALSE)
points(max_ent[,1], max_ent[,2], col="blue")
#par(new=TRUE)
#plot(sgd[,1], sgd[,2], col="green", xaxt='n', yaxt='n', ann=FALSE)
points(sgd[,1], sgd[,2], col="green")
#par(new=TRUE)
#plot(svm[,1], svm[,2], col="purple", xaxt='n', yaxt='n', ann=FALSE)
points(svm[,1], svm[,2], col="purple")

axis(side=2, las=1, ylim=c(0, max_time))

legend("topleft", col=c("red", "blue", "green", "purple"), 
       legend=c("Naive Bayes", "Maximum Entropy", "Stochastic Gradient Descent", "Support Vector Machines"),
       cex=.7, pch=1, pt.cex = 1)	
title("Algorithm Run Time by Number of Tweets")

# Plot the Naive Bayes algoritm over the whole data set

full_naive_bayes = as.matrix(read.csv(paste(base_directory, "naive_bayes_whole_dataset.txt", sep=""), header=FALSE))

plot(full_naive_bayes[,1], full_naive_bayes[,3], xlab="Number of Trial Tweets", 
     ylab="Accuracy", type="p", col="blue")

title("Naive Bayes Trials on Whole Go Data Set")


# Plot the differences in accuracy for SGD 
# over different values of alpha (a training parameter)

sgd_alpha = as.matrix(read.csv(paste(base_directory, "sgd_alpha.txt", sep=""), header=FALSE))

plot(sgd_alpha[,3], sgd_alpha[,4], xlab="Alpha", 
     ylab="Accuracy", type="p", col="blue")

title("SGD Performance by Training Parameter Alpha")



# Plot the differences in accuracy for SGD 
# over different values of l1_ratio (a training parameter)

sgd_alpha = as.matrix(read.csv(paste(base_directory, "sgd_l1_ratio.txt", sep=""), header=FALSE))

plot(sgd_alpha[,3], sgd_alpha[,4], xlab="L1 Ratio", 
     ylab="Accuracy", type="p", col="blue")

title("SGD Performance by Training Parameter L1 Ratio")



# Plot the svm data over different numbers of points and different algorithms

svm_data = as.matrix(read.csv(paste(base_directory, "svm_kernel.txt", sep=""), header=FALSE))

# Get the data for each algorithm
svm_linear_data = svm_data[1:10,]
svm_rbf_data = svm_data[11:20,]
svm_poly_data = svm_data[21:30,]



max_accuracy = max(max(svm_linear_data[,4]),max(svm_rbf_data[,4]), max(svm_poly_data[,4]))
min_accuracy = min(min(svm_linear_data[,4]), min(svm_rbf_data[,4]), min(svm_poly_data[,4]))
plot(svm_linear_data[,1], svm_linear_data[,4], xlab="Number of Trial Tweets", ylab="Accuracy", 
     type="p", col="red", yaxt='n', ylim=c(0, 1))
par(new=TRUE)
points(svm_rbf_data[,1], svm_rbf_data[,4], col="blue")
par(new=TRUE)
points(svm_poly_data[,1], svm_poly_data[,4], col="green")

axis(side=2, las=1, ylim=c(0, max_accuracy))

legend("topleft", col=c("red", "blue", "green"), 
       legend=c("Linear Kernel", "RBF Kernel", "Polynomial Kernel (degree 3)"),
       cex=.6, pch=1, pt.cex = 1)	
title("Accuracy of SVM Kernels by Number of Tweets")





# Plot the differences in accuracy for Maximum Entropy over different numbers
# of iterations

maxent_iterations = as.matrix(read.csv(paste(base_directory, "maxent_iterations.txt", sep=""), header=FALSE))

plot(maxent_iterations[,3], maxent_iterations[,4], xlab="Iterations", 
     ylab="Accuracy", type="p", col="blue")

title("Maximum Entropy Accuracy By Number of Iterations (1000 Trail Tweets)")
