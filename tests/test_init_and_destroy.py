
import os
import shutil
import subprocess
import filerecords.api.settings as settings

os.chdir( os.path.dirname( __file__ ) )

def test_first_init():

    shutil.rmtree( settings.registry_dir, ignore_errors = True )

    cmd = "records init"
    out = subprocess.run( cmd, shell=True, capture_output = True )
    
    assert out.returncode == 0, f"{out.returncode=} instead of 0"
    assert os.path.exists( settings.registry_dir ), "registry is not being created!"
    assert os.path.exists( os.path.join( settings.registry_dir, settings.indexfile ) ), "registry indexfile is not being created!"
    assert os.path.exists( os.path.join( settings.registry_dir, settings.registry_metafile ) ), "registry metafile is not being created!"

def test_second_init():

    shutil.rmtree( settings.registry_dir, ignore_errors = True )

    cmd = "records init"
    out = subprocess.run( cmd, shell=True, capture_output=True )
    out = subprocess.run( cmd, shell=True, capture_output=True )
    
    assert out.returncode == 0, f"{out.returncode=} instead of 0"
    assert "already exists" in out.stdout.decode(), f"{out.stdout.decode()=} does not contain 'already exists'"

def test_init_with_comment():

    shutil.rmtree( settings.registry_dir, ignore_errors = True )

    cmd = "records init -c 'testcomment'"
    out = subprocess.run( cmd, shell=True, capture_output = True )
    
    assert out.returncode == 0, f"{out.returncode=} instead of 0"
    assert os.path.exists( settings.registry_dir ), "registry is not being created!"
    
    with open( os.path.join( settings.registry_dir, settings.registry_metafile ), "r" ) as f:
        contents = f.read()

    assert "testcomment" in contents

def test_init_with_flag_group():

    shutil.rmtree( settings.registry_dir, ignore_errors = True )

    cmd = "records init -g testgroup1 : test1 test2 -g testgroup2 : test3 test4"
    out = subprocess.run( cmd, shell=True, capture_output=True )
    
    assert out.returncode == 0, f"{out.returncode=} instead of 0"
    assert os.path.exists( settings.registry_dir ), "registry is not being created!"
    
    with open( os.path.join( settings.registry_dir, settings.registry_metafile ), "r" ) as f:
        contents = f.read()

    assert "test1" in contents
    assert "group:testgroup2" in contents


def test_init_with_flag_group_and_comment():

    shutil.rmtree( settings.registry_dir, ignore_errors = True )

    cmd = "records init -c 'testcomment' -g testgroup1 : test1 test2 -g testgroup2 : test3 test4"
    out = subprocess.run( cmd, shell=True, capture_output=True )
    
    assert out.returncode == 0, f"{out.returncode=} instead of 0"
    assert os.path.exists( settings.registry_dir ), "registry is not being created!"
    
    with open( os.path.join( settings.registry_dir, settings.registry_metafile ), "r" ) as f:
        contents = f.read()

    assert "testcomment" in contents
    assert "test2" in contents
    assert "group:testgroup2" in contents


def test_destroy():

    shutil.rmtree( settings.registry_dir, ignore_errors = True )

    cmd = "records init"
    out = subprocess.run( cmd, shell=True, capture_output=True )
    
    assert out.returncode == 0, f"{out.returncode=} instead of 0"
    assert os.path.exists( settings.registry_dir ), "registry is not being created!"
    
    cmd = "records destroy -y"
    out = subprocess.run( cmd, shell=True, capture_output=True )
    
    assert out.returncode == 0, f"{out.returncode=} instead of 0"
    assert not os.path.exists( settings.registry_dir ), "registry is not being destroyed!"

def test_clear():

    shutil.rmtree( settings.registry_dir, ignore_errors = True )

    cmd = "records init ; touch testfile ; records comment testfile -c 'testcomment' -f testing"
    out = subprocess.run( cmd, shell=True, capture_output=True )
    
    assert os.path.exists( settings.registry_dir ), "registry is not being created!"
    assert len( os.listdir( settings.registry_dir ) ) == 3, f"registry only contains {len( os.listdir( settings.registry_dir ) )} files instead of 3"
    
    cmd = "records clear -y"
    out = subprocess.run( cmd, shell=True, capture_output=True )
    
    assert os.path.exists( settings.registry_dir ), "registry is being removed!"
    assert len( os.listdir( settings.registry_dir ) ) == 2, f"registry only contains {len( os.listdir( settings.registry_dir ) )} files instead of 2"
    
def test_make_new_in_subdir():

    shutil.rmtree( settings.registry_dir, ignore_errors = True )

    cmd = "records init ;\
            touch testfile_super ; \
            records comment testfile_super -f testflag ; \
            mkdir testsubdir ; \
            cd testsubdir ; \
            touch testfile_sub ; \
            records init ; \
            records comment testfile_sub -f testflag ; \
            cd.. "
    out = subprocess.run( cmd, shell=True, capture_output=True )

    assert os.path.exists( settings.registry_dir ), "parent registry directory does not exist"
    assert os.path.exists( os.path.join( "testsubdir", settings.registry_dir ) ), "subdirectory registry does not exist"

    cmd = "records list -f testflag"
    out = subprocess.run( cmd, shell=True, capture_output=True )

    assert "testfile_super" in out.stdout.decode(), f"{out.stdout.decode()=} does not contain 'testfile_super'"
    assert "testfile_sub" not in out.stdout.decode(), f"{out.stdout.decode()=} also contains 'testfile_sub'"


    cmd = "cd testsubdir ; records list -f testflag"
    out = subprocess.run( cmd, shell=True, capture_output=True )

    assert "testfile_super" not in out.stdout.decode(), f"{out.stdout.decode()=} also contains 'testfile_super'"
    assert "testfile_sub" in out.stdout.decode(), f"{out.stdout.decode()=}  does not contain 'testfile_sub'"


    os.system( "rm -rf testsubdir ; rm testfile*" )