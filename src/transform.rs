use std::collections::HashMap;

use crate::term::Term;

pub struct Transform<'a> {
    name: String,
    inputs: Vec<Term<'a>>,
    output: Term<'a>,
}

impl<'a> Transform<'a> {
    pub fn new(name: String, inputs: Vec<Term<'a>>, output: Term<'a>) -> Self {
        return Transform {
            name,
            inputs,
            output,
        };
    }

    pub fn apply(&self, inputs: Vec<Term<'a>>) -> Term<'a> {
        let mut mapping = HashMap::new();

        // Bind all variables
        for it in self.inputs.iter().zip(inputs.iter()) {
            let (generic, real) = it;

            mapping.extend(generic.bind(real.clone()));
        }

        // Sub variables into output
        let mut out = self.output.clone();

        for (iname, binding) in mapping {
            let temp = out.substitute(iname, binding);
            out = temp;
        }

        out
    }
}
