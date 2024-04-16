# dspreset_to_polyendplay
Convert .dspreset drumkits, to polyend play directory format. 


_Notes_: 
 - currently hardcoded to work with Samples From Mars
 - outputdir must be set directly in the code, at the top.


 # Example
An example. Run from WSL on windows. I used WSL is to have access to the `find` command. 
(The script should work fine in normal windows, though currently untested)

    $ find /mnt/c/Users/bgrav/DecentSampler/out/ -wholename "*Kit*.dspreset" -exec python3 ./dspreset_to_play.py "{}" \;
