#include <iostream>
#include <fstream>
#include <vector>

struct timestamp{
	uint32_t runNumber;
	uint32_t WRCounter;
	uint32_t channel;
	uint32_t seq_id;
	uint64_t sec;
	uint32_t coarse;
	uint32_t frac;
};

void printTS(timestamp ts){
	// std::cout << "runNumber " << ts.runNumber << std::endl;
	// std::cout << "WRCounter " <<ts.WRCounter << std::endl;
	// std::cout << "channel " << ts.channel << std::endl;
	// std::cout << "seq_id " << ts.seq_id << std::endl;
	std::cout << "sec " << ts.sec << std::endl;
	// std::cout << "coarse " << ts.coarse << std::endl;
	// std::cout << "frac " << ts.frac << std::endl;
}

int main(int argc, char *argv[]){
	//Parse options
	if(argc != 2){
		std::cout << "readToConsole takes exactly one argument" << std::endl;
		exit(-1);
	}	

	//Open file
	std::ifstream infile;
	infile.open(argv[1], std::ios::binary | std::ios::in);

	//Deserialize
	infile.seekg(0, infile.end);
	int length = infile.tellg();
	infile.seekg(0, infile.beg);
	std::vector<uint32_t> data;
	data.resize(length/sizeof(uint32_t));
	if(!infile.read((char*)&data[0], length)){
		std::cout << "COULD NOT READ" << std::endl;
	}

	std::vector<timestamp> timestamps;

	for(int i=0; i < data.size()/7; i++){
		timestamp ts;
		ts.runNumber = data.at(i*7);
		ts.WRCounter = data.at(i*7+1);
		ts.channel = data.at(i*7+2);
		ts.seq_id = data.at(i*7+3);
		ts.sec = data.at(i*7+4);
		ts.coarse = data.at(i*7+5);
		ts.frac = data.at(i*7+6);
		printTS(ts);
		timestamps.push_back(ts);
	}

	//Do something with the timestamps :) 

	return 0;
}