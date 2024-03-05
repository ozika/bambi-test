import os, json 
from groo.groo import get_root
import bammm.bammm as mm
import bambi as bmb

root_dir = get_root(".hidden_root")
db_path = os.path.join(root_dir, "databse_name.json")
models_path = os.path.join(root_dir, "models")

mm.models_init(db_path)

models = json.load(open(db_path, "r"))

# load data that come with bambi
data = bmb.load_data("sleepstudy")

model_family = "sleepstudy" # this will be used as a folder name to host the models
model_identifier = "maximum_model"

mod = mm.get_template()
# dependent variable
mod["lmm"]["dep_var"] = "Reaction" # Reaction time
# fixed effects
mod["lmm"]["fxeff"] = ["Days"] # longitudinal data set
# random effects
mod["lmm"]["rneff"] = ["Days|Subject"]
# build equation
mod["lmm"]["eq"] = mm.generate_equation(mod["lmm"]["dep_var"], mod["lmm"]["fxeff"], mod["lmm"]["rneff"])

# fitting information
mod["est"]["nchains"] = 2
mod["est"]["nsamples"] = 1000
mod["est"]["ncores"] = 2 # number of cores to be useds in fitting

mod = mm.prepare_fit(mod, model_family, model_identifier, models_path)
mod["current_sys_location"] = mod["location"]
# save model (it's a good idea to load/save the DB often, especially if one runs multiple models at the same time)
models[mod["name"]] = mod
mm.save_model_info(models, db_path)

mod, results, m = mm.estimate_lmm(mod, data, override=0)
mm.update_model_entry(models, mod, db_path)