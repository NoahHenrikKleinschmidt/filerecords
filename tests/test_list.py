
import os
import shutil
import subprocess
import filerecords.api.settings as settings

def setup():
    os.chdir( os.path.dirname( __file__ ) )
    shutil.rmtree( settings.registry_dir, ignore_errors = True )

    cmd = " mkdir testsubdir ; \
            touch testsubdir/__testfile ; \
            touch testfile1 ; \
            records init ; \
            records comment testfile1 -c 'upper testfile' -f upper ; \
            records comment testsubdir/__testfile -c 'testsubdir testfile' -f lower ; \
            "
    out = subprocess.run( cmd, shell=True, capture_output = True )

def cleanup():
    cmd = "records destroy -y ; \
            rm -rf testfile1 testsubdir ; \
            "
    out = subprocess.run( cmd, shell=True, capture_output = True )
   


def test_global_list():

    setup()

    cmd = "records list"
    out = subprocess.run( cmd, shell=True, capture_output = True )

    assert "No search criteria" in out.stdout.decode(), "Search criteria info is missing from output"
    assert "testfile1" in out.stdout.decode(), "testfile not in list"
    assert "testsubdir/__testfile" in out.stdout.decode(), "testsubdir/__testfile not in list"

    assert "(upper)" in out.stdout.decode(), "upper flag not in list"
    assert "(lower)" in out.stdout.decode(), "lower flag not in list"

    cleanup()

def test_search_flag_list():

    setup()

    cmd = "records list -f upper"
    out = subprocess.run( cmd, shell=True, capture_output = True )

    assert "No search criteria" not in out.stdout.decode(), "Search criteria info still in output"
    assert "testfile1" in out.stdout.decode(), "testfile not in list"
    assert "testsubdir/__testfile" not in out.stdout.decode(), "testsubdir/__testfile is also in the list"

    assert "(upper)" in out.stdout.decode(), "upper flag not in list"
    assert "(lower)" not in out.stdout.decode(), "lower flag is also in the list"

    cleanup()

def test_search_pattern_list():

    setup()

    cmd = "records list -e __"
    out = subprocess.run( cmd, shell=True, capture_output = True )

    assert "No search criteria" not in out.stdout.decode(), "Search criteria info still in output"
    assert "testfile1" not in out.stdout.decode(), "testfile is also in the list"
    assert "testsubdir/__testfile" in out.stdout.decode(), "testsubdir/__testfile not in list"

    assert "(upper)" not in out.stdout.decode(), "upper flag is also in the list"
    assert "(lower)" in out.stdout.decode(), "lower flag not in list"

    cleanup()

def test_localdir_global_list():

    setup()

    cmd = "records ls"
    out = subprocess.run( cmd, shell=True, capture_output = True )

    assert "No search criteria" in out.stdout.decode(), "Search criteria info is missing from output"
    assert "testfile1" in out.stdout.decode(), "testfile not in list"
    assert "testsubdir/__testfile" not in out.stdout.decode(), "testsubdir/__testfile is also in the list"

    assert "(upper)" in out.stdout.decode(), "upper flag not in list"
    assert "(lower)" not in out.stdout.decode(), "lower flag is also in the list"

    cleanup()

def test_localdir_search_flag_list():

    setup()

    cmd = "records ls -f newflag"
    out = subprocess.run( cmd, shell=True, capture_output = True )

    assert "No records found" in out.stdout.decode(), "No records found message is missing from output"
    assert "testfile1" not in out.stdout.decode(), "testfile is also in the list"
    assert "testsubdir/__testfile" not in out.stdout.decode(), "testsubdir/__testfile is also in the list"

    cleanup()

def test_search_both():

    setup()
    
    cmd = "touch testfile3 ; records comment testfile3 -f upper ; records list -f upper -e 3"
    out = subprocess.run( cmd, shell=True, capture_output = True )

    assert "No search criteria" not in out.stdout.decode(), "Search criteria info still in output"
    assert "testfile3" in out.stdout.decode(), "testfile3 is not in the list"
    assert "testfile1" not in out.stdout.decode(), "testfile is also in the list"
    assert "testsubdir/__testfile" not in out.stdout.decode(), "testsubdir/__testfile is also in the list"

    assert "(upper)" in out.stdout.decode(), "upper flag not in list"
    assert "(lower)" not in out.stdout.decode(), "lower flag is also in the list"

    os.remove( "testfile3" )
    cleanup()

def test_localdir_search_both():

    setup()

    cmd = "touch testfile3 ; records comment testfile3 -f upper ; records ls -f upper -e 3"
    out = subprocess.run( cmd, shell=True, capture_output = True )

    assert out.returncode == 0, f"{out.returncode=} instead of 0"

    assert "No search criteria" not in out.stdout.decode(), "Search criteria info still in output"
    assert "testfile3" in out.stdout.decode(), "testfile3 is not in the list"
    assert "testfile1" not in out.stdout.decode(), "testfile is also in the list"
    assert "testsubdir/__testfile" not in out.stdout.decode(), "testsubdir/__testfile is also in the list"

    assert "(upper)" in out.stdout.decode(), "upper flag not in list"
    assert "(lower)" not in out.stdout.decode(), "lower flag is also in the list"

    os.remove( "testfile3" )
    cleanup()