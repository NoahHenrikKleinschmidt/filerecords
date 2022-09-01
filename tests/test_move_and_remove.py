
import os
import shutil
import subprocess
import filerecords.api.settings as settings

os.chdir( os.path.dirname( __file__ ) )
shutil.rmtree( settings.registry_dir, ignore_errors = True )

cmd = "mkdir testsubdir ; touch testsubdir/testfile ; touch testfile ; records init ; records comment testfile -c 'the testfile testing comment' -f testing"
out = subprocess.run( cmd, shell=True, capture_output = True )


def test_move_with():

    cmd = "records mv testfile testfile2"
    out = subprocess.run( cmd, shell=True, capture_output = True )

    assert out.returncode == 0, f"{out.returncode=} instead of 0"

    with open( os.path.join( settings.registry_dir, settings.indexfile ), "r" ) as f:
        contents = f.read()
    
    assert "testfile2\t" in contents, "new filename appears not in indexfile"
    assert "testfile\t" not in contents, "old filename appears in indexfile"
    assert os.path.exists( "testfile2" ), "file was not moved since new path does not exists"
    assert not os.path.exists( "testfile" ), "file was not moved since old path still exists"

def test_move_without():

    cmd = "records mv -k testfile2 testfile"
    out = subprocess.run( cmd, shell=True, capture_output = True )

    assert out.returncode == 0, f"{out.returncode=} instead of 0"

    with open( os.path.join( settings.registry_dir, settings.indexfile ), "r" ) as f:
        contents = f.read()
    
    assert "testfile\t" in contents, "new filename appears not in indexfile"
    assert "testfile2\t" not in contents, "old filename appears in indexfile"
    assert os.path.exists( "testfile2" ), "file was moved since old path does not exists"
    assert not os.path.exists( "testfile" ), "file was moved since new path exists"

    os.rename( "testfile2", "testfile" )

def test_remove_without():

    cmd = "records rm -k testfile"
    out = subprocess.run( cmd, shell=True, capture_output = True )

    assert out.returncode == 0, f"{out.returncode=} instead of 0"

    with open( os.path.join( settings.registry_dir, settings.indexfile ), "r" ) as f:
        contents = f.read()
    
    assert not "testfile" in contents, "filename still appears in indexfile"
    assert os.path.exists( "testfile" ), "file removed since path does not exists"

    os.system( "records comment testfile -c 'the testfile testing comment' -f testing" )

def test_remove_with():

    with open( os.path.join( settings.registry_dir, settings.indexfile ), "r" ) as f:
        contents = f.read()
    
    assert "testfile" in contents, "filename not in indexfile to begin with"

    cmd = "records rm testfile"
    out = subprocess.run( cmd, shell=True, capture_output = True )

    assert out.returncode == 0, f"{out.returncode=} instead of 0"

    with open( os.path.join( settings.registry_dir, settings.indexfile ), "r" ) as f:
        contents = f.read()
    
    assert not "testfile" in contents, "filename still appears in indexfile"
    assert not os.path.exists( "testfile" ), "file not removed since path does still exists"

    os.system( "touch testfile ; records comment testfile -c 'the testfile testing comment' -f testing" )

def test_move_in_subdir():

    cmd = "records mv testfile testsubdir/testfile2"
    out = subprocess.run( cmd, shell=True, capture_output = True )

    assert out.returncode == 0, f"{out.returncode=} instead of 0"

    with open( os.path.join( settings.registry_dir, settings.indexfile ), "r" ) as f:
        contents = f.read()
    
    assert "testsubdir/testfile2" in contents, "new filename appears not in indexfile"
    assert "testfile\t" not in contents, "old filename appears in indexfile"
    assert os.path.exists( "testsubdir/testfile2" ), "file was not moved since new path does not exists"
    assert not os.path.exists( "testfile" ), "file was not moved since old path still exists"


    cmd = "cd testsubdir ; records mv testfile2 ../testfile ; cd .."
    out = subprocess.run( cmd, shell=True, capture_output = True )

    assert out.returncode == 0, f"{out.returncode=} instead of 0"

    with open( os.path.join( settings.registry_dir, settings.indexfile ), "r" ) as f:
        contents = f.read()
    
    assert "testfile\t" in contents, "new filename appears not in indexfile"
    assert "testsubdir/testfile2" not in contents, "old filename appears in indexfile"
    assert os.path.exists( "testfile" ), "file was not moved since new path does not exists"
    assert  not os.path.exists( "testsubdir/testfile2" ), "file was not moved since old path still exists"
