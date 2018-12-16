use regex::Regex;
use std::collections::HashMap;
use std::collections::HashSet;
use std::env;
use std::fmt;
use std::fs;
use std::process::Command;
struct AnalysisRes {
    call_pairs: HashMap<String, HashSet<String>>,
    node_fn: HashMap<String, String>,
}
impl fmt::Display for AnalysisRes {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(
            f,
            "There are {} functions, and {} call pairs",
            self.node_fn.len(),
            self.call_pairs
                .iter()
                .fold(0, |sum, (_, value)| sum + value.len())
        );
        for (node, function) in self.node_fn.iter() {
            write!(f, "Node {} equals to function {}\n", node, function);
        }
        for (node, function_calls) in self.call_pairs.iter() {
            let caller = self.node_fn.get(node).unwrap();
            for callee in function_calls {
                write!(
                    f,
                    "Function {} called function {}\n",
                    caller,
                    self.node_fn
                        .get(callee)
                        .unwrap_or(&String::from("UNKNOW FUNCTION"))
                );
            }
        }
        write!(f, "")
    }
}
fn demangle(mangled: &str) -> String {
    String::from_utf8(
        Command::new("c++filt")
            .arg("-n")
            .arg(mangled)
            .output()
            .expect("Fail to demangle")
            .stdout,
    )
    .expect("Fail to convert")
}
fn analyse(dotcontent: &str, regex_vec: &Vec<Regex>) -> AnalysisRes {
    let node_regex = &regex_vec[1];
    let dir_regex = &regex_vec[2];
    let mut call_pairs_map = HashMap::new();
    let mut node_fn_map = HashMap::new();
    for node in node_regex.captures_iter(dotcontent) {
        call_pairs_map.insert(String::from(&node["node_name"]), HashSet::new());
        node_fn_map.insert(
            String::from(&node["node_name"]),
            demangle(&node["label_name"]),
        );
        println!("Node {} inserted", &node["node_name"]);
    }
    for direct in dir_regex.captures_iter(dotcontent) {
        println!(
            "From {} to {} inserted",
            &direct["s_node"], &direct["e_node"]
        );
        call_pairs_map
            .get_mut(&direct["s_node"])
            .unwrap()
            .insert(String::from(&direct["e_node"]));
    }
    let res = AnalysisRes {
        call_pairs: call_pairs_map,
        node_fn: node_fn_map,
    };
    res
}
fn stack_expansion(
    stack_trace: HashSet<String>,
    call_pairs_map: &HashMap<String, HashSet<String>>,
    depth: u32,
) -> HashSet<String> {
    let mut res = HashSet::new();
    let next_set = &mut HashSet::new();
    let pre_set = &mut HashSet::new();
    pre_set.extend(stack_trace.iter().cloned());
    res.extend(stack_trace.iter().cloned());
    for i in 0..depth {
        println!("-------In depth {}-------", i);
        for x in pre_set.iter() {
            next_set.extend(call_pairs_map[x].iter().cloned());
            res.extend(next_set.iter().cloned());
        }
        pre_set.clear();
        std::mem::swap(next_set, pre_set);
    }
    println!("Total {} node inserted", res.len());
    res
}
fn read_regex(filename: &str) -> Vec<Regex> {
    let regex_text = fs::read_to_string(filename).expect("Regex reading error");
    let v: Vec<&str> = regex_text.split("\n").collect();
    let regex_vec: Vec<Regex> = v.iter().map(|x| Regex::new(x).unwrap()).collect();
    regex_vec
}
fn main() {
    let args: Vec<String> = env::args().collect();
    let filename = &args[1];
    let regex = &args[2];
    let contents = &fs::read_to_string(filename).expect("Some thing is wrong");
    let regex_vec = read_regex(regex);

    println!("Doing call_pairs");
    let res = analyse(contents, &regex_vec);
    println!("{}", res);
    let _fail_trace = stack_expansion(
        res.call_pairs.get("Node0x5642d48d0890").unwrap().clone(),
        &res.call_pairs,
        1,
    );
}
