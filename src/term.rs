use std::{
    collections::{HashMap, HashSet},
    fmt::Display,
};

use crate::transform::Transform;

pub enum Structure {
    Generic(String),
    Defined(String, u8),
}

impl PartialEq for Structure {
    fn eq(&self, other: &Self) -> bool {
        match (self, other) {
            (Structure::Generic(name1), Structure::Generic(name2)) => name1 == name2,
            (Structure::Defined(name1, arity1), Structure::Defined(name2, arity2)) => {
                (name1 == name2) && (arity1 == arity2)
            }
            _ => false,
        }
    }
}

#[derive(Clone)]
pub struct Term<'a> {
    pub strct: &'a Structure,
    args: Vec<Term<'a>>,
}

#[derive(Clone)]
pub enum Unit<'a> {
    Term(Term<'a>),
    Call(Box<Transform<'a>>, Vec<Term<'a>>),
    CallSelf(Vec<Term<'a>>),
}

impl<'a> Unit<'a> {
    pub fn substitute(&self, iname: &String, real: Term<'a>) -> Unit<'a> {
        match self {
            Unit::Term(term) => Unit::Term(term.substitute(iname, real)),
            Unit::Call(transform, args) => Unit::Call(
                transform.clone(),
                args.iter()
                    .map(|a| a.substitute(iname, real.clone()))
                    .collect(),
            ),
            Unit::CallSelf(args) => Unit::CallSelf(
                args.iter()
                    .map(|a| a.substitute(iname, real.clone()))
                    .collect(),
            ),
        }
    }
}

impl<'a> Term<'a> {
    pub fn new(strct: &'a Structure, args: Vec<Term<'a>>) -> Self {
        return Term { strct, args };
    }

    pub fn bind(&self, real: Term<'a>) -> HashMap<&String, Term<'a>> {
        let mut map = HashMap::new();

        match self.strct {
            Structure::Generic(name) => {
                map.insert(name, real);
            }
            Structure::Defined(_, _) => {
                if self.strct == real.strct {
                    for (idx, arg) in self.args.iter().enumerate() {
                        match arg.strct {
                            Structure::Generic(name) => {
                                let real_value = real.args.get(idx).unwrap();
                                map.insert(name, real_value.clone());
                            }
                            Structure::Defined(_, _) => {
                                let real_value = real.args.get(idx).unwrap();
                                let bindings = arg.bind(real_value.clone());

                                map.extend(bindings);
                            }
                        }
                    }
                }
            }
        }

        return map;
    }

    pub fn unique_generics(&self) -> HashSet<String> {
        let mut generics = HashSet::new();

        match self.strct {
            Structure::Generic(name) => {
                generics.insert(name.clone());
            }
            Structure::Defined(_, _) => {
                for arg in self.args.iter() {
                    generics.extend(arg.unique_generics());
                }
            }
        }

        return generics;
    }

    pub fn substitute(&self, iname: &String, real: Term<'a>) -> Term<'a> {
        match self.strct {
            Structure::Generic(name) => {
                if name == iname {
                    return real.clone();
                } else {
                    return self.clone();
                }
            }
            Structure::Defined(_, _) => {
                let mut new_args = Vec::new();

                for arg in self.args.iter() {
                    let subed = arg.substitute(&iname, real.clone());
                    new_args.push(subed);
                }

                let updated = Term::new(self.strct, new_args);

                return updated.clone();
            }
        }
    }
}

impl<'a> Display for Term<'a> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self.strct {
            Structure::Generic(name) => {
                return write!(f, "{}", name);
            }
            Structure::Defined(name, _) => {
                let args: Vec<String> = self.args.iter().map(|a| a.to_string()).collect();
                return write!(f, "{}({})", name, args.join(", "));
            }
        }
    }
}
