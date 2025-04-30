# BRLAN editing

This documentation is copied from SDR (huge thanks to robojumper).
The diff has been updated for HD's pause_00_sekiban.brlan.
https://github.com/ssrando/ssrando/blob/main/docs/tablets-brlan.md

In order for the randomizer to display the correct tablets and gemstones
in the pause menu (instead of a fixed order - Emerald, Ruby, Amber),
the randomizer requires patches to the brlan file that contains UI animation
data in a binary format. This document describes what changes were made,
since the changed binary file cannot be inspected. Robo wanted the process
to be reproducible in case someone wants to touch this file again and I fully
agree. Again, thank you very much Robo for documenting this process!

Required tools:

* [BrawlCrate](https://github.com/soopercool101/BrawlCrate)
* [Benzin](https://horizon.miraheze.org/wiki/Benzin)

* Open `romfs/Layout/MenuPause.arc` with BrawlCrate
* Extract `anim/pause_00_sekiban.brlan` in BrawlCrate
* Run `.\BENZIN.exe r pause_00_sekiban.brlan pause_00_sekiban.xmlan`

Apply the following changes:

```xml
diff --git a/./pause_00_sekiban.orig.xmlan b/tst/pause_00_sekiban.xmlan
index 343b6cf..eaa6ec0 100644
--- a/./pause_00_sekiban.orig.xmlan
+++ b/./pause_00_sekiban.xmlan
@@ -11,7 +11,7 @@
                                        <string>G_sekiban_00</string>
                                </seconds>
                        </pat1>
-                       <pai1 framesize="5" flags="00">
+                       <pai1 framesize="8" flags="00">
                                <timg name="hm_moleGloveA_00.tpl" />
                                <timg name="hm_moleGloveB_00.tpl" />
                                <timg name="hm_swordA_00.tpl" />
@@ -35,6 +35,10 @@
                                <timg name="uk_purseC_00.tpl" />
                                <timg name="uk_purseD_00.tpl" />
                                <timg name="uk_purseE_00.tpl" />
+                               <timg name="tr_sekiban_03.tpl" />
+                               <timg name="tr_sekiban_04.tpl" />
+                               <timg name="tr_sekiban_05.tpl" />
+                               <timg name="tr_sekiban_06.tpl" />
                                <pane name="P_shadow_00" type="0">
                                        <tag type="RLVI">
                                                <entry type1="0" type2="Visibility">
@@ -198,7 +202,7 @@
                                                                <padding>0000</padding>
                                                        </pair>
                                                        <pair>
-                                                               <data1>3.000000000000000</data1>
+                                                               <data1>7.000000000000000</data1>
                                                                <data2>0000</data2>
                                                                <padding>0000</padding>
                                                        </pair>
@@ -1271,6 +1275,11 @@
                                                                <data2>0001</data2>
                                                                <padding>0000</padding>
                                                        </pair>
+                                                       <pair>
+                                                               <data1>4.000000000000000</data1>
+                                                               <data2>0000</data2>
+                                                               <padding>0000</padding>
+                                                       </pair>
                                                </entry>
                                        </tag>
                                </pane>
@@ -1287,6 +1296,16 @@
                                                                <data2>0001</data2>
                                                                <padding>0000</padding>
                                                        </pair>
+                                                       <pair>
+                                                               <data1>3.000000000000000</data1>
+                                                               <data2>0000</data2>
+                                                               <padding>0000</padding>
+                                                       </pair>
+                                                       <pair>
+                                                               <data1>5.000000000000000</data1>
+                                                               <data2>0001</data2>
+                                                               <padding>0000</padding>
+                                                       </pair>
                                                </entry>
                                        </tag>
                                </pane>
@@ -1303,6 +1322,11 @@
                                                                <data2>0001</data2>
                                                                <padding>0000</padding>
                                                        </pair>
+                                                       <pair>
+                                                               <data1>6.000000000000000</data1>
+                                                               <data2>0000</data2>
+                                                               <padding>0000</padding>
+                                                       </pair>
                                                </entry>
                                        </tag>
                                </pane>
@@ -1699,6 +1723,26 @@
                                                                <data2>000d</data2>
                                                                <padding>0000</padding>
                                                        </pair>
+                                                       <pair>
+                                                               <data1>3.000000000000000</data1>
+                                                               <data2>0014</data2>
+                                                               <padding>0000</padding>
+                                                       </pair>
+                                                       <pair>
+                                                               <data1>4.000000000000000</data1>
+                                                               <data2>0017</data2>
+                                                               <padding>0000</padding>
+                                                       </pair>
+                                                       <pair>
+                                                               <data1>5.000000000000000</data1>
+                                                               <data2>0018</data2>
+                                                               <padding>0000</padding>
+                                                       </pair>
+                                                       <pair>
+                                                               <data1>6.000000000000000</data1>
+                                                               <data2>0019</data2>
+                                                               <padding>0000</padding>
+                                                       </pair>
                                                </entry>
                                        </tag>
                                </pane>
```

* Run `.\BENZIN.exe w pause_00_sekiban.xmlan pause_00_sekiban.brlan`

Now you have a brlan file that works with the rando patches (cf. get_tablet_keyframe_count)
