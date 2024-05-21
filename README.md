# alembic_scripts
## Getting started with Alembic
### What is Alembic?
Because SQLAlchemy does not natively support migrations beyond adding and deleting tables, it is not possible to modify tables without refreshing the database. Alembic adds support for migrations, allowing tables to be modified and changed without affecting the data in the DB

### Installing Alembic
To install Alembic, just `pip install alembic`

## Using Alembic
### Initialization
To initialize alembic, cd to the directory containing model.py and run `alembic init alembic`
* The alembic following init will be the name of the directory created by the command so it can be anything

You should be left with a directory structure similar to this:
tethysapp-test\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── install.yml\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── setup.py\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── tethysapp\
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── test\
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── alembic\
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── env.py\
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── __pycache__\
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── README\
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── script.py.mako\
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── versions\
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── alembic.ini\
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── alembic_scripts.py\
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── app.py\
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── controllers.py\
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── __init__.py\
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── model.py\

### Modifying alembic/env.py

#### target_metadata
1. Import any model from model.py
2. Set target_meta equal to the model's metadata attribute
    * Example: `target_metadata = Base.metadata`

#### GeoAlchemy2 Support
Alembic does not natively support external modules such as geoalchemy2. There are multiple ways to deal with these problems, and this is a specific solution for geoalchemy2
1. At the top of env.py: `from geoalchemy2 import alembic_helpers`
2. run_migrations_offline() and run_migrations_online() both have `context.configure(...)` within them. In both of these functions' context.configure, add `include_object=alembic_helpers.include_object, process_revision_directives=alembic_helpers.writer, render_item=alembic_helpers.render_item`

## Using alembic_scripts.py
### Modifying model.py
1. Import alembic_scripts.py
2. In the database initializer, after Base.metadata.create_all(engine), add calls to alembic_scripts methods.
    * These will be run when `tethys syncstores app` when put within the initializer
### Methods
1. alembic_engine: modifies the alembic.ini file to point to the engine
2. alembic_revision: creates autogenerated revisions and upgrades the database
3. alembic_suite: Calls other methods
#### Parameters:
1. engine: the engine
2. path: String - absolute path to alembic.ini
3. resolution: Boolean
    * True: os.path.abspath() called on provided path and existence is checked
    * False: skip abspath and existence check. Only useful for relative path.


