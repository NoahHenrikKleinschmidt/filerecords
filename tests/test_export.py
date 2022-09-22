
import os
import shutil
import subprocess
import filerecords.api.settings as settings

def setup():
    os.chdir( os.path.dirname( __file__ ) )
    shutil.rmtree( settings.registry_dir, ignore_errors = True )

    cmd = " mkdir testsubdir ; \
            touch testsubdir/__testfile ; \
            touch testfile ; \
            records init ; \
            records comment -c 'registrycomment' -f registryflag ; \
            records comment testfile -c 'secret_super_testfile' -f upper ; \
            records comment testsubdir/__testfile -c 'great_other_testfile' -f lower ; \
            "
    out = subprocess.run( cmd, shell=True, capture_output = True )

def cleanup():
    cmd = "records destroy -y ; \
            rm -rf testfile testsubdir *.md *.yaml ; \
            "
    out = subprocess.run( cmd, shell=True, capture_output = True )

def test_export_md():

    setup()

    before = os.listdir()
    cmd = "records export md"
    out = subprocess.run( cmd, shell=True, capture_output = True )
    after = os.listdir()

    assert len(after) == len(before) + 1, "no new file created"

    mdfile = [ f for f in after if f not in before ][0]
    assert mdfile.endswith(".md"), "file is not markdown"

    with open( mdfile, "r" ) as f:
        contents = f.read()
    
    assert "registryflag" in contents, "registryflag not in the output"
    assert "secret_super_testfile" in contents, "secret_super_testfile not in the output"
    assert "great_other_testfile" in contents, "great_other_testfile not in the output"
    assert "upper" in contents, "upper not in the output"

    cleanup() 

def test_export_md_withfilename():

    setup()

    before = os.listdir()
    cmd = "records export md -f testfile.md"
    out = subprocess.run( cmd, shell=True, capture_output = True )
    after = os.listdir()

    assert len(after) == len(before) + 1, "no new file created"

    mdfile = [ f for f in after if f not in before ][0]
    assert mdfile.endswith(".md"), "file is not markdown"

    with open( mdfile, "r" ) as f:
        contents = f.read()
    
    assert "registryflag" in contents, "registryflag not in the output"
    assert "secret_super_testfile" in contents, "secret_super_testfile not in the output"
    assert "great_other_testfile" in contents, "great_other_testfile not in the output"
    assert "upper" in contents, "upper not in the output"

    cleanup() 

def test_export_yml():

    setup()

    before = os.listdir()
    cmd = "records export yaml"
    out = subprocess.run( cmd, shell=True, capture_output = True )
    after = os.listdir()

    assert len(after) == len(before) + 1, "no new file created"

    yamlfile = [ f for f in after if f not in before ][0]
    assert yamlfile.endswith(".yaml"), "file is not markdown"

    with open( yamlfile, "r" ) as f:
        contents = f.read()
    
    assert "registryflag" in contents, "registryflag not in the output"
    assert "secret_super_testfile" in contents, "secret_super_testfile not in the output"
    assert "great_other_testfile" in contents, "great_other_testfile not in the output"
    assert "upper" in contents, "upper not in the output"

    cleanup() 

def test_export_yml_with_filename():

    setup()

    before = os.listdir()
    cmd = "records export yaml -f testfile.yml"
    out = subprocess.run( cmd, shell=True, capture_output = True )
    after = os.listdir()

    assert len(after) == len(before) + 1, "no new file created"

    yamlfile = [ f for f in after if f not in before ][0]
    assert yamlfile.endswith(".yaml"), "file is not markdown"

    with open( yamlfile, "r" ) as f:
        contents = f.read()
    
    assert "registryflag" in contents, "registryflag not in the output"
    assert "secret_super_testfile" in contents, "secret_super_testfile not in the output"
    assert "great_other_testfile" in contents, "great_other_testfile not in the output"
    assert "upper" in contents, "upper not in the output"

    cleanup() 

def test_export_both():

    setup()

    before = os.listdir()
    cmd = "records export both"
    out = subprocess.run( cmd, shell=True, capture_output = True )
    after = os.listdir()

    assert len(after) == len(before) + 2, "no new files created"

    cleanup() 

def test_export_both_with_filename():

    setup()

    before = os.listdir()
    cmd = "records export both -f testfile"
    out = subprocess.run( cmd, shell=True, capture_output = True )
    after = os.listdir()

    assert len(after) == len(before) + 2, "no new files created"

    cleanup() 