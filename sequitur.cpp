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
	unordered_map<int, vector<int>> codeCache; // key: starting block of trace, val: trace	
	string file = "bbls";
	int occurenceThreshold = 2;
	int windowSize = 500;

	string runSequitur(string &history) {
		string cmd = "echo \"" + history + "\" | ./sequitur -q -d -r -p -k " + to_string(occurenceThreshold);		
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

public:	
	void process() {
		ifstream ifs(file);
		string history, line;
		int count = 0, count2 = 0;
		while (getline(ifs, line)) {
			history += line + '\n';
			count++;
			if (count == windowSize) {				
				updateCodeCache(history);
				count = 0;
				history.clear();
				//debugging output
				count2++;
				cerr << count2 << endl;
			}			
		}
		ifs.close();
	}

	void printCodeCache() {
		int length = 0;
		for (auto &p : codeCache) {
			length += p.second.size();
			/*for (int &num : p.second) {
				cout << num << ' ';
			}
			cout << endl;*/
		}
		length /= codeCache.size();
		cout << "average length: " << length << endl;
	}
};

int main () {
	Sequitur sequitur;
	sequitur.process();
	sequitur.printCodeCache();
}