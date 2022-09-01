
import os
import shutil
import subprocess
import filerecords.api.settings as settings

os.chdir( os.path.dirname( __file__ ) )
shutil.rmtree( settings.registry_dir, ignore_errors = True )

cmd = "records init"
out = subprocess.run( cmd, shell=True, capture_output = True )


def test_comment_registry():

    cmd = "records comment -c 'testcomment'"
    out = subprocess.run( cmd, shell=True, capture_output = True )

    assert out.returncode == 0, f"{out.returncode=} instead of 0"

    with open( os.path.join( settings.registry_dir, settings.registry_metafile ), "r" ) as f:
        contents = f.read()

    assert "testcomment" in contents, f"test comment appears not in metafile... {contents=}"

def test_flag_registry():

    cmd = "records comment -f superflag1"
    out = subprocess.run( cmd, shell=True, capture_output = True )

    assert out.returncode == 0, f"{out.returncode=} instead of 0"

    with open( os.path.join( settings.registry_dir, settings.registry_metafile ), "r" ) as f:
        contents = f.read()

    assert "superflag1" in contents, f"test flag appears not in metafile... {contents=}"

def test_comment_firsttime_file():

    cmd = "touch testfile ; records comment -c 'testcomment' testfile"
    out = subprocess.run( cmd, shell=True, capture_output = True )

    assert out.returncode == 0, f"{out.returncode=} instead of 0"

    with open( os.path.join( settings.registry_dir, settings.indexfile ), "r" ) as f:
        contents = f.read()

    assert "testfile" in contents, "filename appears not in indexfile"

    regfile = os.listdir( settings.registry_dir )
    regfile.remove( settings.registry_metafile )
    regfile.remove( settings.indexfile )

    assert len( regfile ) == 1, f"len(regfile) != 1, {len(regfile)=}"

    regfile = regfile[0]
    regfile = os.path.join( settings.registry_dir, regfile )

    with open( regfile, "r" ) as f:
        contents = f.read()
    
    assert "testcomment" in contents


def test_comment_secondtime_file():

    cmd = "records comment testfile -f superflag22"
    out = subprocess.run( cmd, shell=True, capture_output = True )

    assert out.returncode == 0, f"{out.returncode=} instead of 0"

    regfile = os.listdir( settings.registry_dir )
    regfile.remove( settings.registry_metafile )
    regfile.remove( settings.indexfile )

    assert len( regfile ) == 1

    regfile = regfile[0]
    regfile = os.path.join( settings.registry_dir, regfile )

    with open( regfile, "r" ) as f:
        contents = f.read()
    
    assert "testcomment" in contents, f"test comment appears not in metafile... {contents=}"
    assert "superflag22" in contents, f"test flag appears not in metafile... {contents=}"

def test_comment_from_subdir():
    

    cmd = "mkdir testsubdir ; cd testsubdir ; touch testfile; records comment testfile -c 'another testile' ; cd .. "
    out = subprocess.run( cmd, shell=True, capture_output = True )

    assert out.returncode == 0, f"{out.returncode=} instead of 0"

    regfile = os.listdir( settings.registry_dir )
    regfile.remove( settings.registry_metafile )
    regfile.remove( settings.indexfile )

    assert len( regfile ) == 2, f"len(regfile) != 2, {len(regfile)=}"

    with open( os.path.join( settings.registry_dir, settings.indexfile ), "r" ) as f:
        contents = f.read()
    
    assert "testsubdir" in contents, f"the subdir-located file does not appear with a proper path..."

    os.system( "cd testsubdir ; records rm -k testfile" )

def test_comment_in_subdir():

    cmd = "mkdir testsubdir ; cd testsubdir ; touch testfile; cd .. ; records comment testsubdir/testfile -c 'another testile' "
    out = subprocess.run( cmd, shell=True, capture_output = True )

    assert out.returncode == 0, f"{out.returncode=} instead of 0"

    regfile = os.listdir( settings.registry_dir )
    regfile.remove( settings.registry_metafile )
    regfile.remove( settings.indexfile )

    assert len( regfile ) == 2, f"len(regfile) != 2, {len(regfile)=}"

    with open( os.path.join( settings.registry_dir, settings.indexfile ), "r" ) as f:
        contents = f.read()
    
    assert "testsubdir" in contents, f"the subdir-located file does not appear with a proper path..."

    os.system( "records rm -k testsubdir/testfile" )


def test_flag_registry():

    cmd = "records flag -f superflag29"
    out = subprocess.run( cmd, shell=True, capture_output = True )

    assert out.returncode == 0, f"{out.returncode=} instead of 0"

    with open( os.path.join( settings.registry_dir, settings.registry_metafile ), "r" ) as f:
        contents = f.read()

    assert "superflag29" in contents, f"test flag appears not in metafile... {contents=}"

def test_flag_record():

    cmd = "records flag testfile -f superflag29"
    out = subprocess.run( cmd, shell=True, capture_output = True )

    assert out.returncode == 0, f"{out.returncode=} instead of 0"

    regfile = os.listdir( settings.registry_dir )
    regfile.remove( settings.registry_metafile )
    regfile.remove( settings.indexfile )

    assert len( regfile ) == 1

    regfile = regfile[0]
    regfile = os.path.join( settings.registry_dir, regfile )

    with open( regfile, "r" ) as f:
        contents = f.read()
    
    assert "superflag29" in contents, f"test flag appears not in metafile... {contents=}"

def test_define_group():

    cmd = "records flag --group supergroup : super1 super7"
    out = subprocess.run( cmd, shell=True, capture_output = True )

    assert out.returncode == 0, f"{out.returncode=} instead of 0"

    with open( os.path.join( settings.registry_dir, settings.registry_metafile ), "r" ) as f:
        contents = f.read()
    
    assert "supergroup" in contents, f"test group appears not in metafile... {contents=}"
    assert "super1" in contents, f"test flag appears not in metafile... {contents=}"
    assert "super7" in contents, f"test flag appears not in metafile... {contents=}"
    assert "group:supergroup" in contents, f"group:testgroup flag appears not in metafile... {contents=}"

def test_undo_flag():

    cmd = "records comment -c 'comment_to_leave' -f flag_to_undo"
    out = subprocess.run( cmd, shell=True, capture_output = True )

    assert out.returncode == 0, f"{out.returncode=} instead of 0"

    with open( os.path.join( settings.registry_dir, settings.registry_metafile ), "r" ) as f:
        contents = f.read()
    
    assert "flag_to_undo" in contents, f"test flag appears not in metafile... {contents=}"
    assert "comment_to_leave" in contents, f"test comment appears not in metafile... {contents=}"

    cmd = "records undo -f flag_to_undo"
    out = subprocess.run( cmd, shell=True, capture_output = True )

    assert out.returncode == 0, f"{out.returncode=} instead of 0"

    with open( os.path.join( settings.registry_dir, settings.registry_metafile ), "r" ) as f:
        contents = f.read()
    
    assert "flag_to_undo" not in contents, f"test flag still appears in metafile... {contents=}"
    assert "comment_to_leave" in contents, f"test comment was also removed from metafile... {contents=}"

def test_undo_comment():

    cmd = "records comment -c 'comment_to_undo' -f flag_to_leave"
    out = subprocess.run( cmd, shell=True, capture_output = True )

    assert out.returncode == 0, f"{out.returncode=} instead of 0"

    with open( os.path.join( settings.registry_dir, settings.registry_metafile ), "r" ) as f:
        contents = f.read()
    
    assert "comment_to_undo" in contents, f"test flag appears not in metafile... {contents=}"
    assert "flag_to_leave" in contents, f"test flag appears not in metafile... {contents=}"

    cmd = "records undo"
    out = subprocess.run( cmd, shell=True, capture_output = True )

    assert out.returncode == 0, f"{out.returncode=} instead of 0"

    with open( os.path.join( settings.registry_dir, settings.registry_metafile ), "r" ) as f:
        contents = f.read()
    
    assert "comment_to_undo" not in contents, f"test flag still appears in metafile... {contents=}"
    assert "flag_to_leave" in contents, f"test flag was also removed from metafile... {contents=}"


shutil.rmtree( settings.registry_dir, ignore_errors = True )
os.system( "rm testfile*" )
os.system( "rm -rf testsubdir" )