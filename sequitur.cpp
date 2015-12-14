#include <fstream>
#include <sstream>
#include <iostream>
#include <string>
#include <map>
#include <unordered_map>
#include <vector>
#include <cstdlib>
#include <cstdio>

using namespace std;

class Sequitur {
private:	
	string INPUT_FILE = "bbls";
	int OCCURRENCE_THRESHOLD = 3;
	int WINDOW_SIZE = 500;

	unordered_map<int, vector<int>> codeCache; // key: starting block of trace, val: trace
	int hitBlock = 0;
	int totalBlock = 0;
	int idealTrace = 0;
	int totalTrace = 0;	

	void updateCodeCache(string &history) {
		string pattern = runSequitur(history);
		vector<string> patterns;
		istringstream iss(pattern);
		string line;
		while (getline(iss, line)) {
			//cout << line << endl;
			patterns.push_back(line);
		}		

		unordered_map<int, vector<int>> patternMap;
		for (int i = patterns.size() - 1; i > 0; i--) {
			string line = patterns[i];
			istringstream iss2(line);
			int idx;
			iss2 >> idx;

			int tabIdx = line.find('\t');
			string patternStr = line.substr(tabIdx);
			//cout << idx << ": " << patternStr << endl;
			iss2.clear();
			iss2.str(patternStr);
			string num;
			while (iss2 >> num) {
				//cout << num << " ";
				patternMap[idx].push_back(stoi(num.substr(1, num.size() - 1)));
			}
			//cout << endl;
		}
		
		map<int, vector<vector<int>>> orderedPatternMap;
		for (auto &p : patternMap) {
			orderedPatternMap[p.second.size()].push_back(p.second);
		}
		for (auto it = orderedPatternMap.rbegin(); it != orderedPatternMap.rend(); ++it) {
			for (vector<int> &trace : it->second) {
				int head = trace[0], idx = 0, size;
				bool longer = false;
				//cout << "trace size: " << trace.size() << endl;
				while (idx < trace.size() && codeCache.find(head) != codeCache.end()) {
					//cout << "!" << endl;
					size = 0;
					while (idx < trace.size() && size < codeCache[head].size() && codeCache[head][size] == trace[idx]) {
						idx++;
						size++;
					}
					if (size == codeCache[head].size()) {
						longer = true;
						break;
					}
					if (idx < trace.size()) {
						head = trace[idx];
					}					
				}
				if (longer) {
					codeCache[head] = vector<int>(trace.begin() + idx - size, trace.end());
				} else if (idx < trace.size()) {
					codeCache[head] = vector<int>(trace.begin() + idx, trace.end());
				}
			}
		}
	}

	string runSequitur(string &history) {
		string cmd = "echo \"" + history + "\" | ./sequitur -q -d -r -p -k " + to_string(OCCURRENCE_THRESHOLD);		
		FILE *fp = popen(cmd.c_str(), "r");
       	if(!fp){
         	cerr << "Could not open pipe for output." << endl;
         	exit(0);
       	}
       	char buffer[100];
		string result;	
		while (fgets(buffer, 100, fp)) {
			result += buffer;
	    }
	    pclose(fp);	    
	    return result;
	}

	void collectStats(vector<int> &bbls) {
		int i = 0;
		while (i < bbls.size()) {
			if (codeCache.find(bbls[i]) != codeCache.end()) {				
				vector<int> trace = codeCache[bbls[i]];
				int idx = 0;
				while (idx < trace.size() && i < bbls.size() && bbls[i] == trace[idx]) {
					hitBlock++;
					totalBlock++;
					idx++;
					i++;
				}
				if (idx == trace.size()) {
					idealTrace++;
				}
				totalTrace++;
			} else {
				totalBlock++;
				i++;
			}
		}			
	}

public:	
	void process() {
		ifstream ifs(INPUT_FILE);
		string history, line;
		int count = 0, count2 = 0;
		vector<int> bbls;
		while (getline(ifs, line)) {
			history += line + '\n';
			bbls.push_back(stoi(line));
			count++;
			if (count == WINDOW_SIZE) {
				collectStats(bbls);
				updateCodeCache(history);
				count = 0;
				history.clear();
				bbls.clear();

				//debugging output
				if (count2 % 100 == 0) {
					cout << count2 << endl;
					printStats();
				}
				count2++;						
			}
		}
		ifs.close();
	}

	void printStats() {
		cout << "bbl hit rate: " << double(hitBlock) / totalBlock * 100 << '%' << endl;
		cout << "ideal trace rate: " << double(idealTrace) / totalTrace * 100 << '%' << endl;
		int length = 0;
		for (auto &p : codeCache) {
			length += p.second.size();
		}
		cout << "average trace length: " << double(length) / codeCache.size() << endl;
	}

	void printCodeCache() {
		cout << "code cache size: " << codeCache.size() << endl;
		for (auto &p : codeCache) {			
			cout << "trace: ";
			for (int &num : p.second) {
				cout << num << ' ';
			}
			cout << endl;
		}		
	}
};

int main () {
	Sequitur sequitur;
	sequitur.process();	
	//sequitur.printCodeCache();
	sequitur.printStats();
}