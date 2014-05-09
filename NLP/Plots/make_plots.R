# The first column is the number of input tweets
# the second column is the percent correct
base_directory = "C:\\Users\\Louis\\thetweetrises\\NLP\\Plots\\"
naive_bayes = as.matrix(read.csv(base_directory + "naive_bayes_file_1.txt"))
max_ent = as.matrix(read.csv(base_directory + "naive_bayes_file_1.txt"))
sgd = as.matrix(read.csv(base_directory + "sgd_file_1.txt"))
svm = as.matrix(read.csv(base_directory + "svm_file_1.txt"))

plot(n_mat, xlab="Number of Trial Tweets", ylab="Accuracy %", type="p")
title("Accuracy by Number of Tweets")