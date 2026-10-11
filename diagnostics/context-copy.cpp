#include <nift/nift.h>
#include <chrono>
#include <iostream>
int main(){
 for(int records : {0,10,100,1000,10000}){
  nift::Value data=nift::Value::make_object(),list=nift::Value::make_array();
  for(int i=0;i<records;i++){nift::Value item=nift::Value::make_object();item["id"]=nift::Value(i);item["name"]=nift::Value("record-"+std::to_string(i));list.push_back(item);}data["records"]=list;
  nift::Context context;context.set("d",data);nift::Engine engine;
  for(int defaults=0;defaults<2;defaults++){
   if(defaults)engine.set("d",data);
   for(int sample=-2;sample<10;sample++){
    auto start=std::chrono::steady_clock::now();
    for(int i=0;i<100;i++){auto result=defaults?engine.render_text("literal"):engine.render_text("literal",context);if(!result.ok()||result.output()!="literal")return 1;}
    auto ns=std::chrono::duration_cast<std::chrono::nanoseconds>(std::chrono::steady_clock::now()-start).count();
    std::cout<<"{\"records\":"<<records<<",\"binding\":\""<<(defaults?"engine-default":"request-context")<<"\",\"sample\":"<<sample<<",\"batch\":100,\"ns\":"<<ns<<"}\n";
   }
  }
 }
}
