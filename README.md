# DIY Island

Step-by-step guide to an interactive map for your very own
remote island!

## Software
* Python
* TileMill
* QGIS or GDAL (optional)

## Get Geodata
If you want your island to look realistic, it helps to start with an actual coastline.
Be careful to use a small or lesser-known area. Most of your audience would recognize the
state of Florida, but fewer would know the Florida Keys or the many islands of Oceania.

### Sources
You can download national borders in GeoJSON format from https://github.com/johan/world.geo.json/

You can download coastlines in OSM or SHP format from http://downloads.cloudmade.com/

## Alter Geodata

### Choose Features
Going back to the Florida Keys map, let's say that you are only adding one or two to the
map. In QGIS, you can use "Select Features by Freehand" to draw around the shapes which
you want.

<img src="https://raw.github.com/mapmeld/diy-island/gh-pages/screenshots/select_in_qgis.png"/>

Then use "Layer > Save Selection as Vector File..." to save the highlighted areas.

<img src="https://raw.github.com/mapmeld/diy-island/gh-pages/screenshots/save_selection_qgis.png"/>

In the Save dialog, select GeoJSON format, and use Browse to select what to name the
saved file.

<img src="https://raw.github.com/mapmeld/diy-island/gh-pages/screenshots/save_geojson_qgis.png"/>

### Edit Coastline
In QGIS, use Layer > Toggle Editing to make each point moveable. This option only
works on shapefiles. If you do not have a shapefile, right-click the layer in the sidebar,
save as an ESRI Shapefile, and open that file in QGIS.

When you are done making edits, click Layers > Toggle Editing again, and you will have
a choice to save or undo your changes.

Right-click the layer in the sidebar and save as GeoJSON.

### Rotate and Flip
To make the original borders less obvious, you might want to rotate or flip your map.

If you do not have a GeoJSON file, either skip this step or use a GIS tool (QGIS or GDAL)
to convert the file to GeoJSON.

Use the Python script in this repo to change your file.

    python mapflip.py source.geojson --flip_horizontal
    python mapflip.py source.geojson --flip_vertical
    python mapflip.py source.geojson --rotate 90

Currently the only rotation options are 90, 180, and 270 degrees clockwise

## Style a Map
Open TileMill and create a new project. Do not include the world map data.

### Prepare Project
* Click the Layers menu in the bottom left, and click Add Layer.
* Select your final map file (shapefile or GeoJSON format) and then Save & Style
* Center your map on your data. For small areas, it may be difficult to find at first. Change style.mss for your layer to have line-width:50; and click Save or Ctrl+S. A blob should appear.

<img src="https://raw.github.com/mapmeld/diy-island/gh-pages/screenshots/blot_tilemill.png"/>

* Click the wrench in the top right of TileMill to set your project boundaries. Continue zooming to the center of the blob until you can see a defined shape.
* Click shift and drag the mouse to frame the area. Click inside the box to set the project center. Credit OpenStreetMap in the attribution. Move the minimum and maximum zoom bars (a zoom level number is visible in the top left of your map). Click Save.

<img src="https://raw.github.com/mapmeld/diy-island/gh-pages/screenshots/project_settings_tilemill.png"/>

* If your project is made of several LineStrings, the coastline may not form a consistent shape. Run linemeet.py in this repo to make a polygon out of the lines.
        python linemeet.py

<img src="https://raw.github.com/mapmeld/diy-island/gh-pages/screenshots/jagged_tilemill.png"/>

* Quit and re-open TileMill to see your changes.

### Use Carto-CSS
A good starting point for style.mss might be
```
Map {
  background-color: #486ea6;
}
#island {
  line-color:#594;
  line-width:0.5;
  polygon-opacity:1;
  polygon-fill:#ae8;
}
```

Where #island is the id of your map layer.

Add dimension by putting these two attributes inside the island style:

```
building-fill:#ae8;
building-height: -0.005;
```

<img src="https://raw.github.com/mapmeld/diy-island/gh-pages/screenshots/carto_tilemill.png"/>

Depending on the scale and shape of the islands, you might want a positive, negative, much higher, or much lower value for building-height.

Change the colors to fit the tone of your island. Bright and shiny? Mysterious?

### Add more layers
If you downloaded shapefiles from Cloudmade, you'll find several other layers. Natural features
like rivers and lakes are good. If your island has infrastructure, you can include the
highways (roads) layer. Apply the same rotate / flip operation and style them differently.

Click and drag layers inside of the layers menu to change the stacking order (so roads
display over rivers, for example).

### Use Textures
The water and land could use some textures! Go to the Documents/MapBox/projects folder and
find your project. Go looking for a water.png and land.png, where land.png should be a mostly
transparent, only lightly textured thing. Then add this to your stylesheet:

```
Map {
  background-image: url('water.png');
}
#island {
  polygon-pattern-file: url('land.jpg');
}
```

If you are using building-height, that part will remain untextured by polygon-pattern-file.

<img src="https://raw.github.com/mapmeld/diy-island/gh-pages/screenshots/texture_tilemill.png"/>


## Add Labels
If you want to add labels (static, not interactive data) to your map, continue using
TileMill. To skip ahead to interactive markers, go to the next step.

### GeoJSON
Add points to the original location on the world map using http://geojson.io

On each point, have a label property with what you want to be labeled.

Save the GeoJSON file locally and run the same commands using mapflip.py if you flipped or rotated the map.

Add the GeoJSON file to TileMill, and use a marker-labeling code such as

```
#labels {
  marker-width:10;
  marker-fill:#f45;
  marker-line-color:#813;
  marker-allow-overlap: true;
  ::label {
    text-name: [label];
    text-face-name: "Didot Regular";
    text-size: 25;
    text-fill: #fff;
    text-allow-overlap: true;
    text-dy: 10;
  }
}
```

<img src="https://raw.github.com/mapmeld/diy-island/gh-pages/screenshots/label_tilemill.png"/>

You can use any font on your computer in TileMill, and it will create tiles which others can see,
even if they don't have the same font installed.

### Rare Languages
Maybe it's not enough for you to have your own island. No problem! The next step lets you
have your own language.

Instead of making an alphabet from scratch, you can insert characters from rare, existing
languages. If you're afraid of someone understanding your work, you can even use a few
undeciphered alphabets which have been added to Unicode. The script in this repo supports
random letters from several languages, but you may need a font from Omniglot for the
letters to appear on your map. Try "Arial Regular" and other standard fonts first, because
they have the most language support.

I ran the script against my labels.geojson, asking it to replace the 'sample' attribute.
If it has a word four letters long, like 'Home', it will be replaced by four random
characters from Tifinagh.

    python rarelang.py labels.geojson --field sample --language tifinagh

Currently supporting Tifinagh and Mongolian. For any other alphabet, set a
range of Unicode characters.

    python rarelang.py labels.geojson --field sample --range "0x0400-0x04AA"

<img src="https://raw.github.com/mapmeld/diy-island/gh-pages/screenshots/cycle_letters_tilemill.png"/>

If you don't like your random letters, re-run the script, click the eye in the layers tool
to hide the labels, save, click the eye again to reload the labels, save, and your new
combination will appear.

## Upload to MapBox

Create an account on <a href="http://mapbox.com">MapBox.com</a>, and verify your e-mail.

<img src="https://raw.github.com/mapmeld/diy-island/gh-pages/screenshots/export_tilemill.png"/>

Back in TileMill, click the Export menu in the top right. Select Upload. You will be
given a change to update your project boundaries and upload size. Review the options, then
click Upload.

<img src="https://raw.github.com/mapmeld/diy-island/gh-pages/screenshots/upload_to_mapbox.png"/>

If you experience issues, go to the Export menu again and click View exports to try again,
or export MBTiles and upload the tiles using MapBox tools.

## Add Markers

MapBox has updated their map editor a bit so you can add plenty of markers in a user-friendly
way. Don't use any Baselayer, because it won't match up with your fictional maps!

<img src="https://raw.github.com/mapmeld/diy-island/gh-pages/screenshots/mapbox_label.png"/>
<img src="https://raw.github.com/mapmeld/diy-island/gh-pages/screenshots/mapbox_color.png"/>

Click "Untitled map" to change that to something awesome:

<img src="https://raw.github.com/mapmeld/diy-island/gh-pages/screenshots/mapbox_click_untitled.png"/>
<img src="https://raw.github.com/mapmeld/diy-island/gh-pages/screenshots/mapbox_description.png"/>


## Share Your Map

<img src="https://raw.github.com/mapmeld/diy-island/gh-pages/screenshots/mapbox_share.png"/>

Click Share and you'll find a link that you can send out into an unsuspecting world. Congratulations!
