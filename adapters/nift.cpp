#include <nift/nift.h>
#include <chrono>
#include <fstream>
#include <iostream>
#include <sstream>
#include <map>
#include <vector>
#include <filesystem>
std::string read(const std::filesystem::path&p){std::ifstream f(p,std::ios::binary);if(!f)throw std::runtime_error("missing "+p.string());return {std::istreambuf_iterator<char>(f),{}};}
int main(int argc,char**argv){try{
 auto root=std::filesystem::path(argv[1]);std::string mode=argv[2];int batch=std::stoi(argv[3]),samples=std::stoi(argv[4]),renders=std::stoi(argv[5]),distinct=std::stoi(argv[6]);
 nift::Engine engine;engine.set_root(root/"nift");nift::Context contexts[2];for(int i=0;i<2;i++)if(!contexts[i].set_json("d",read(root/("data"+std::to_string(i)+".json"))))throw std::runtime_error("JSON binding rejected");
 std::map<std::string,std::string> texts;for(auto &entry:std::filesystem::directory_iterator(root/"nift"))texts[entry.path().filename().string()]=read(entry.path());
 if(mode!="files")engine.set_loader(std::function<std::optional<std::string>(std::string_view)>([&](std::string_view path)->std::optional<std::string>{auto it=texts.find(std::filesystem::path(path).filename().string());return it==texts.end()?std::nullopt:std::optional<std::string>(it->second);}));
 std::string expected[2]={read(root/"expected0.txt"),read(root/"expected1.txt")};
 auto op=[&](){std::vector<std::string> outputs;for(int i=0;i<renders*distinct;i++){int k=i%distinct;auto result=mode=="files"?engine.render_path(root/"nift"/("main"+std::to_string(k)),contexts[i%2]):engine.render_text(texts.at("main"+std::to_string(k)),contexts[i%2]);if(!result.ok())throw std::runtime_error(result.error().message);outputs.push_back(result.output());}return outputs;};
 if(mode=="fresh"){for(auto &out:op())std::cout<<out;return 0;}
 for(int sample=-2;sample<samples;sample++){std::vector<std::vector<std::string>> outputs;auto start=std::chrono::steady_clock::now();for(int b=0;b<batch;b++)outputs.push_back(op());auto ns=std::chrono::duration_cast<std::chrono::nanoseconds>(std::chrono::steady_clock::now()-start).count();for(auto &group:outputs)for(size_t i=0;i<group.size();i++){auto exp=expected[i%2]+(distinct>1?"<!--"+std::to_string(i%distinct)+"-->":"");if(group[i]!=exp)throw std::runtime_error("incorrect output: "+group[i].substr(0,100)+" expected "+exp.substr(0,100));}std::cout<<"{\"sample\":"<<sample<<",\"warmup\":"<<(sample<0?"true":"false")<<",\"ns\":"<<ns<<",\"batch\":"<<batch<<",\"operations\":"<<batch*renders*distinct<<"}\n"<<std::flush;}
 }catch(const std::exception&e){std::cerr<<e.what()<<"\n";return 1;}}
