#include"map.h"
#include<cstdio>
#include<string>
#include<iostream>

std::string debugOutput;
int Ai_work(const Map& mainGame) {
	debugOutput = "";
	int res = -1;
	for (int i = 0; i < mainGame.getWidth(); i++) {
		if (mainGame.judgeValidity(0, i)) {
			if (res == -1 || mainGame.getTop(res) > mainGame.getTop(i)) {
				res = i;
			}
			debugOutput += std::to_string(i);
		}
	}
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