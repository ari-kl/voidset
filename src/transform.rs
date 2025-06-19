use std::collections::{HashMap, HashSet};

use crate::term::{Structure, Term, Unit};

#[derive(Clone)]
pub struct Transform<'a> {
    name: String,
    cases: Vec<Case<'a>>,
}

#[derive(Clone)]
pub struct Case<'a> {
    inputs: Vec<Term<'a>>,
    output: Unit<'a>,
}

impl<'a> Case<'a> {
    pub fn new(inputs: Vec<Term<'a>>, output: Unit<'a>) -> Self {
        Case { inputs, output }
    }

    pub fn matches(&self, reals: &Vec<Term<'a>>) -> bool {
        for (input, real) in self.inputs.iter().zip(reals.iter()) {
            match (input.strct, real.strct) {
                (Structure::Defined(name1, arity1), Structure::Defined(name2, arity2)) => {
                    if !((name1 == name2) && (arity1 == arity2)) {
                        return false;
                    }
                }
                _ => {}
            }
        }

        return true;
    }
}

impl<'a> Transform<'a> {
    pub fn new(name: String, cases: Vec<Case<'a>>) -> Self {
        return Transform { name, cases };
    }

    pub fn apply(&self, inputs: Vec<Term<'a>>) -> Option<Term<'a>> {
        for input in &inputs {
            print!("{}, ", input)
        }
        println!();

        for (idx, case) in self.cases.iter().enumerate() {
            if case.matches(&inputs) {
                println!("match case {}", idx);
                let mut mapping = HashMap::new();

                // Bind all variables
                for it in case.inputs.iter().zip(inputs.iter()) {
                    let (generic, real) = it;

                    mapping.extend(generic.bind(real.clone()));
                }

                // Sub variables into output
                let mut out = case.output.clone();

                for (iname, binding) in mapping {
                    let temp = out.substitute(iname, binding);
                    out = temp;
                }

                return match out {
                    Unit::Term(term) => Some(term),
                    Unit::Call(transform, args) => transform.apply(args),
                    Unit::CallSelf(args) => self.apply(args),
                };
            }
        }

        return None;
    }
}
