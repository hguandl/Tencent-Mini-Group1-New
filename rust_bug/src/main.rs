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
    fn_node: HashMap<String, String>
}
impl fmt::Display for AnalysisRes {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(
            f,
            "There are {} functions, and {} call pairs\n",
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
    str::replace(mangled,"\\l","")
}
fn analyse(dotcontent: &str, regex_vec: &Vec<Regex>) -> AnalysisRes {
    let node_regex = &regex_vec[1];
    let dir_regex = &regex_vec[2];
    let mut call_pairs_map = HashMap::new();
    let mut node_fn_map = HashMap::new();
    let mut fn_node_map = HashMap::new();
    for node in node_regex.captures_iter(dotcontent) {
        call_pairs_map.insert(String::from(&node["node_name"]), HashSet::new());
        node_fn_map.insert(
            String::from(&node["node_name"]),
            demangle(&node["label_name"]),
        );
        fn_node_map.insert(
            String::from(&node["label_name"]),
            demangle(&node["node_name"])
            );
    }
    for direct in dir_regex.captures_iter(dotcontent) {
            call_pairs_map
            .get_mut(&direct["s_node"])
            .unwrap()
            .insert(String::from(&direct["e_node"]));
    }
    let res = AnalysisRes {
        call_pairs: call_pairs_map,
        node_fn: node_fn_map,
        fn_node: fn_node_map
    };
    res
}
fn stack_expansion(
    stack_trace: HashSet<String>,
    call_pairs_map: &HashMap<String, HashSet<String>>,
    depth: u32,
) -> Vec<HashSet<String>> {
    let mut res = Vec::new();
    let next_set = &mut HashSet::new();
    let pre_set = &mut HashSet::new();
    pre_set.extend(stack_trace.iter().cloned());
    res.push(stack_trace.clone());
    for i in 0..depth {
        println!("-------In depth {}-------", i);
        for x in pre_set.iter() {
            if call_pairs_map.contains_key(x) {
                next_set.extend(call_pairs_map[x].iter().cloned());
            }
        }
        res.push(next_set.clone());
        pre_set.clear();
        std::mem::swap(next_set, pre_set);
    }
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
    let expanding_func = &args[3];
    let contents = &fs::read_to_string(filename).expect("Some thing is wrong");
    let regex_vec = read_regex(regex);

    println!("Doing call_pairs\n");
    let res = analyse(contents, &regex_vec);
    let fail_trace = stack_expansion(
        res.call_pairs.get("Node1").unwrap().clone(),
        &res.call_pairs,
        5,
    );
    println!("{}\n",res);
    for (idx, set) in fail_trace.iter().enumerate() {
        println!("In depth {}, {} Functions",idx,set.len())
    }
}
