#include"map.h"
#include<queue>
#include<cstdio>
#include<cassert>
#include<string>
#include<iostream>
#include<algorithm>
#define INF 1e90

const double WeightNow = 0;
std::string debugOutput;
double Valuation(const Map& mainGame) {
	int playerNumber = mainGame.getPlayerNumber();
	int* scoreList = new int[playerNumber];
	mainGame.calcScore(scoreList);
	double value = 1.* (scoreList[0] + 1) / (scoreList[1] + 1);
	return value;
	for (int i = 0; i < mainGame.getWidth(); i++) {
		for (int j = 0; j < mainGame.getTop(i); j++) {
			if (mainGame.getCell(j, i) == 0) {
				for (int k = 0; k < ScoreRoadNumber; k++) {
					if (mainGame.validCoord(j + ScoreRoad[k][0], i + ScoreRoad[k][1]) && mainGame.getCell(j + ScoreRoad[k][0], i + ScoreRoad[k][1]) == 0) {
						value += 0.001;
					}
					if (mainGame.validCoord(j - ScoreRoad[k][0], i - ScoreRoad[k][1]) && mainGame.getCell(j - ScoreRoad[k][0], i - ScoreRoad[k][1]) == 0) {
						value += 0.001;
					}
				}
			}
		}
	}
	return value;
}
double search(const Map& mainGame, int deepth, int& res, int player, double cutValue, int*operaList = NULL) {
	int playerNumber = mainGame.getPlayerNumber();
	std::queue<std::pair<double, int> > opaValue;
	if (player == 0) {
		operaList = new int[playerNumber];
		double maxScore = -INF;
		for (int i = 0; i < mainGame.getWidth(); i++) {
			if (mainGame.judgeValidity(0, i)) {
				operaList[0] = i;
				int opa;
				double score = search(mainGame, 0, opa, 1, maxScore, operaList);

				if (deepth == 0) {
					if (score >= cutValue) {
						delete[] operaList;
						return score;
					}
					if (score > maxScore) {
						maxScore = score;
						res = i;
					}
				}
				else {
					opaValue.push(std::make_pair(score, i));
				}
			}
		}
		if (deepth == 0) {
			if (maxScore == -INF) {
				return Valuation(mainGame);
			}
			return maxScore;
		}
		for (int i = 0; i < 10 && !opaValue.empty(); i++) {
			operaList[0] = opaValue.front().second;
			int opa;
			double score = search(mainGame, deepth, opa, 1, maxScore, operaList);
			if (score >= cutValue) {
				delete[] operaList;
				return score;
			}
			if (score > maxScore) {
				maxScore = score;
				res = opaValue.front().second;
			}
			opaValue.pop();
		}
		delete[] operaList;
		if (maxScore == -INF) {
			return Valuation(mainGame);
		}
		return maxScore;
	}
	else {
		double minScore = INF;
		for (int i = 0; i < mainGame.getWidth(); i++) {
			if (mainGame.judgeValidity(1, i)) {
				Map tmpGame(mainGame);
				operaList[1] = i;
				for (int k = 2; k < playerNumber; k++) {
					operaList[k] = -1;
				}
				tmpGame.doOpeartor(operaList);
				double score = Valuation(tmpGame);

				if (deepth == 0) {
					if (score <= cutValue) {
						return score;
					}
					if (score < minScore) minScore = score;
				}
				else {
					opaValue.push(std::make_pair(-score, i));
				}
			}
		}
		if (deepth == 0) {
			if (minScore == INF) {
				return Valuation(mainGame);
			}
			return minScore;
		}
		for (int i = 0; i < 10 && !opaValue.empty(); i++) {
			Map tmpGame(mainGame);
			operaList[1] = opaValue.front().second;
			for (int k = 2; k < playerNumber; k++) {
				operaList[k] = -1;
			}
			tmpGame.doOpeartor(operaList);
			int opa;
			double score = search(tmpGame, deepth - 1, opa, 0, minScore) * (1 - WeightNow) - opaValue.front().first * WeightNow;
			if (score <= cutValue) return score;
			if (score < minScore) minScore = score;
			opaValue.pop();
		}
		if (minScore == INF) {
			return Valuation(mainGame);
		}
		return minScore;
	}
}
int Ai_work(const Map& mainGame) {
	int playerNumber = mainGame.getPlayerNumber();
	int* operaList = new int[playerNumber];
	int* scoreList = new int[playerNumber];
	debugOutput = "";

	int res = -1;
	search(mainGame, 2, res, 0, INF);
	return res;
}

int main() {
	int height, width, playerNumber, blockNumber, range;
	scanf_s("%d%d%d%d%d", &height, &width, &playerNumber, &blockNumber, &range);
	Map mainGame(height, width, playerNumber, range);
	for (int i = 0; i < blockNumber; i++) {
		int column, row;
		scanf_s("%d%d", &column, &row);
		mainGame.setBlock(column, row);
	}
	int* operaList = new int[playerNumber];

	while (!mainGame.getOver()) {
		operaList[0] = Ai_work(mainGame);
		printf("%d\n", operaList[0]);
		std::cout << debugOutput << std::endl;
		fflush(stdout);
		for (int i = 1; i < playerNumber; i++) {
			scanf_s("%d", operaList + i);
		}
		if (mainGame.doOpeartor(operaList) == 0) {
			mainGame.setOver();
		}
	}
	delete[] operaList;
}