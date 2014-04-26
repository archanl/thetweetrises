from sklearn.linear_model import SGDClassifier
X = [[False, False], [True, True], [True, False], [False, True]]
y = [0, 1, 0, 1]
clf = SGDClassifier(loss="hinge", penalty="l2")
clf.fit(X, y)
res = clf.predict([[False, False]])
print res[0]