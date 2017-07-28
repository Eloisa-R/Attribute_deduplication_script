# Attribute_deduplication_script

Script for data deduplication accross different groups of attributes that had to be merged together.

There were several glossaries of product attributes, with a source value and a translation. When merging them,
we found there were repeated source values but different translations accross the different glossaries.
In order to avoid a human translator going through them to select the right translation, this script selects
the most repeated translation as the definitve one. When there are only two translations to choose from,
the most recent one is selected. Also, before selecting these translations, we get rid of all the translated
values like "multicolor", since it causes problems within the system.
