
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
            rm -rf testfile testsubdir ; \
            "
    out = subprocess.run( cmd, shell=True, capture_output = True )

def test_lookup_registry():

    setup()

    cmd = "records lookup"
    out = subprocess.run( cmd, shell=True, capture_output = True )

    assert "registrycomment" in out.stdout.decode(), "registryflag not in the output"
    assert "secret_super_testfile" not in out.stdout.decode(), "secret_super_testfile is also in the output"
    assert "great_other_testfile" not in out.stdout.decode(), "great_other_testfile is also in the output"

    cleanup()

def test_read_registry():

    setup()

    cmd = "records read"
    out = subprocess.run( cmd, shell=True, capture_output = True )

    assert "registryflag" in out.stdout.decode(), "registryflag not in the output"
    assert "secret_super_testfile" not in out.stdout.decode(), "secret_super_testfile is also in the output"
    assert "great_other_testfile" not in out.stdout.decode(), "great_other_testfile is also in the output"

    cleanup()

def test_lookup_testfile():

    setup()

    cmd = "records lookup testsubdir/__testfile"
    out = subprocess.run( cmd, shell=True, capture_output = True )

    assert "registryflag" not in out.stdout.decode(), "registryflag is also in the output"
    assert "secret_super_testfile" not in out.stdout.decode(), "secret_super_testfile is also in the output"
    assert "great_other_testfile" in out.stdout.decode(), "great_other_testfile not in the output"
    assert "lower" in out.stdout.decode(), "lower flag not in the output"

    cleanup()

def test_read_testfile():

    setup()

    cmd = "records read testfile"
    out = subprocess.run( cmd, shell=True, capture_output = True )

    assert "registryflag" not in out.stdout.decode(), "registryflag is also in the output"
    assert "secret_super_testfile" in out.stdout.decode(), "secret_super_testfile not in the output"
    assert "great_other_testfile" not in out.stdout.decode(), "great_other_testfile is also in the output"
    assert "lower" not in out.stdout.decode(), "lower flag is also in the output"
    assert "upper" in out.stdout.decode(), "upper flag not in the output"
    
    cleanup()

def test_lookup_multiple():

    setup()

    cmd = "records comment testsubdir -c 'thesubdir' ; records lookup test*"
    out = subprocess.run( cmd, shell=True, capture_output = True )

    assert "registryflag" not in out.stdout.decode(), "registryflag is also in the output"
    assert "secret_super_testfile" in out.stdout.decode(), "secret_super_testfile is also in the output"
    assert "great_other_testfile" not in out.stdout.decode(), "great_other_testfile not in the output"
    assert "thesubdir" in out.stdout.decode(), "thesubdir not in the output"

    cleanup()
