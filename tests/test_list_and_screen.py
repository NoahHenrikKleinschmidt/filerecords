
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
    cmd = " records destroy -y ; \
            rm -rf testfile1 testsubdir ; \
            "
    out = subprocess.run( cmd, shell=True, capture_output = True )
   


def test_global_list():

    setup()

    cmd = "records list"
    out = subprocess.run( cmd, shell=True, capture_output = True )

    assert "No search criteria" in out.stdout.decode(), "Search criteria info is missing from output"
    assert "testfile1" in out.stdout.decode(), "testfile not in the output"
    assert "testsubdir/__testfile" in out.stdout.decode(), "testsubdir/__testfile not in the output"

    assert "(upper)" in out.stdout.decode(), "upper flag not in the output"
    assert "(lower)" in out.stdout.decode(), "lower flag not in the output"

    cleanup()

def test_search_flag_list():

    setup()

    cmd = "records list -f upper"
    out = subprocess.run( cmd, shell=True, capture_output = True )

    assert "No search criteria" not in out.stdout.decode(), "Search criteria info still in output"
    assert "testfile1" in out.stdout.decode(), "testfile not in the output"
    assert "testsubdir/__testfile" not in out.stdout.decode(), "testsubdir/__testfile is also in the output"

    assert "(upper)" in out.stdout.decode(), "upper flag not in the output"
    assert "(lower)" not in out.stdout.decode(), "lower flag is also in the output"

    cleanup()

def test_search_pattern_list():

    setup()

    cmd = "records list -e __"
    out = subprocess.run( cmd, shell=True, capture_output = True )

    assert "No search criteria" not in out.stdout.decode(), "Search criteria info still in output"
    assert "testfile1" not in out.stdout.decode(), "testfile is also in the output"
    assert "testsubdir/__testfile" in out.stdout.decode(), "testsubdir/__testfile not in the output"

    assert "(upper)" not in out.stdout.decode(), "upper flag is also in the output"
    assert "(lower)" in out.stdout.decode(), "lower flag not in the output"

    cleanup()

def test_localdir_global_list():

    setup()

    cmd = "records ls"
    out = subprocess.run( cmd, shell=True, capture_output = True )

    assert "No search criteria" in out.stdout.decode(), "Search criteria info is missing from output"
    assert "testfile1" in out.stdout.decode(), "testfile not in the output"
    assert "testsubdir/__testfile" not in out.stdout.decode(), "testsubdir/__testfile is also in the output"

    assert "(upper)" in out.stdout.decode(), "upper flag not in the output"
    assert "(lower)" not in out.stdout.decode(), "lower flag is also in the output"

    cleanup()

def test_localdir_search_flag_list():

    setup()

    cmd = "records ls -f newflag"
    out = subprocess.run( cmd, shell=True, capture_output = True )

    assert "No records found" in out.stdout.decode(), "No records found message is missing from output"
    assert "testfile1" not in out.stdout.decode(), "testfile is also in the output"
    assert "testsubdir/__testfile" not in out.stdout.decode(), "testsubdir/__testfile is also in the output"

    cleanup()

def test_search_both():

    setup()
    
    cmd = "touch testfile3 ; records comment testfile3 -f upper ; records list -f upper -e 3"
    out = subprocess.run( cmd, shell=True, capture_output = True )

    assert "No search criteria" not in out.stdout.decode(), "Search criteria info still in output"
    assert "testfile3" in out.stdout.decode(), "testfile3 is not in the output"
    assert "testfile1" not in out.stdout.decode(), "testfile is also in the output"
    assert "testsubdir/__testfile" not in out.stdout.decode(), "testsubdir/__testfile is also in the output"

    assert "(upper)" in out.stdout.decode(), "upper flag not in the output"
    assert "(lower)" not in out.stdout.decode(), "lower flag is also in the output"

    os.remove( "testfile3" )
    cleanup()

def test_localdir_search_both():

    setup()

    cmd = "touch testfile3 ; records comment testfile3 -f upper ; records ls -f upper -e 3"
    out = subprocess.run( cmd, shell=True, capture_output = True )

    assert out.returncode == 0, f"{out.returncode=} instead of 0"

    assert "No search criteria" not in out.stdout.decode(), "Search criteria info still in output"
    assert "testfile3" in out.stdout.decode(), "testfile3 is not in the output"
    assert "testfile1" not in out.stdout.decode(), "testfile is also in the output"
    assert "testsubdir/__testfile" not in out.stdout.decode(), "testsubdir/__testfile is also in the output"

    assert "(upper)" in out.stdout.decode(), "upper flag not in the output"
    assert "(lower)" not in out.stdout.decode(), "lower flag is also in the output"

    os.remove( "testfile3" )
    cleanup()

def test_screen():

    setup()

    cmd = "records screen"
    out = subprocess.run( cmd, shell=True, capture_output = True )

    assert "testfile1" not in out.stdout.decode(), "testfile1 in the output"
    
    cmd = "mv testfile1 testfile99 ; records screen"
    out = subprocess.run( cmd, shell=True, capture_output = True )

    assert "testfile1" in out.stdout.decode(), "testfile1 is not in the output"
    
    cmd = "records mv -k testfile1 testfile99 ; records screen"
    out = subprocess.run( cmd, shell=True, capture_output = True )

    assert "testfile1" not in out.stdout.decode(), "testfile1 is in the output"
    assert "testfile99" not in out.stdout.decode(), "testfile99 is in the output"
    
    cmd = "records ls"
    out = subprocess.run( cmd, shell=True, capture_output = True )
    
    assert "testfile99" in out.stdout.decode(), "testfile99 is not in the output"

    os.remove( "testfile99" )
    cleanup()