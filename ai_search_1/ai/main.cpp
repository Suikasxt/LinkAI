#include"map.h"
#include<cstdio>
#include<string>
#include<iostream>

std::string debugOutput;
int Ai_work(const Map& mainGame) {
	int playerNumber = mainGame.getPlayerNumber();
	int* operaList = new int[playerNumber];
	int* scoreList = new int[playerNumber];
	debugOutput = "";

	int res = -1;
	int maxScore = -1;
	//枚举所有合法操作，判断在哪个位置落子能够最大化自己的收益
	for (int i = 0; i < mainGame.getWidth(); i++) {
		if (mainGame.judgeValidity(0, i)) {
			debugOutput += std::to_string(i);
			Map tmpGame(mainGame);
			operaList[0] = i;
			for (int j = 1; j < playerNumber; j++) {
				operaList[j] = -1;
			}
			tmpGame.doOpeartor(operaList);
			tmpGame.calcScore(scoreList);

			if (scoreList[0] > maxScore) {
				res = i;
				maxScore = scoreList[0];
			}
		}
	}
	return res;
}

int main() {
	int height, width, playerNumber, blockNumber, range;
	//读入各项参数
	scanf_s("%d%d%d%d%d", &height, &width, &playerNumber, &blockNumber, &range);
	Map mainGame(height, width, playerNumber, range);
	//读入各个初始障碍格
	for (int i = 0; i < blockNumber; i++) {
		int column, row;
		scanf_s("%d%d", &column, &row);
		mainGame.setBlock(column, row);
	}
	int* operaList = new int[playerNumber];

	//主循环
	while (!mainGame.getOver()) {
		//在未知其他各个玩家操作的情况下，决策出自己本回合的决策
		operaList[0] = Ai_work(mainGame);
		printf("%d\n", operaList[0]);
		std::cout << debugOutput << std::endl;
		fflush(stdout);
		//读入其他用户的操作，推进游戏进程
		for (int i = 1; i < playerNumber; i++) {
			scanf_s("%d", operaList + i);
		}
		if (mainGame.doOpeartor(operaList) == 0) {
			mainGame.setOver();
		}
	}
	delete[] operaList;
}