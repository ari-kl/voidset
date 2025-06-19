use crate::{
    term::{Structure, Term},
    transform::Transform,
};

mod term;
mod transform;

fn main() {
    let z = Structure::Defined("Z".to_string(), 0);
    let s = Structure::Defined("S".to_string(), 1);
    let v = Structure::Defined("V".to_string(), 2);

    let zero = Term::new(&z, vec![]);
    let one = Term::new(&s, vec![zero.clone()]);
    let two = Term::new(&s, vec![one.clone()]);

    let a = Structure::Generic("a".to_string());
    let b = Structure::Generic("b".to_string());

    let avar = Term::new(&a, vec![]);
    let bvar = Term::new(&b, vec![]);

    let savar = Term::new(&s, vec![avar.clone()]);
    let sbvar = Term::new(&s, vec![bvar.clone()]);
    let vab = Term::new(&v, vec![avar.clone(), bvar.clone()]);

    let add = Transform::new("add".to_string(), vec![savar, sbvar], vab);
    let result = add.apply(vec![one.clone(), two.clone()]);

    println!("{}", result)
}
