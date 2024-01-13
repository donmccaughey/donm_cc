TMP ?= $(abspath tmp)


.SECONDEXPANSION :


.PHONY : all
all : maze


.PHONY : maze
maze : \
		site-src/maze/maze_bg.wasm \
		site-src/maze/maze_bg.js


.PHONY : upload
upload : $(TMP)/uploaded.stamp.txt


.PHONY : check
check : $(TMP)/checked_html.stamp.txt


.PHONY : clean
clean :
	rm -rf $(TMP)
	rm -rf maze/pkg


site_src := \
		site-src/base.css \
		site-src/robots.txt \
		site-src/aughey/handstand.jpg \
		site-src/banners/Don_and_Molly_hiking_Texas_winter_2016.jpg \
		site-src/banners/Don_and_Molly_Round_Hill_Lake_Tahoe_summer_2019.jpg \
		site-src/banners/Don_and_Molly_San_Francisco_autumn_2021.jpg \
		site-src/business_novels/index.page \
		site-src/c/index.page \
		site-src/engineering_management/index.page \
		site-src/hashtables/index.page \
		site-src/macos_packages/macos_packages.css \
		site-src/make/index.page \
		site-src/maze/maze.css \
		site-src/maze/maze.js \
		site-src/maze/maze_bg.js \
		site-src/maze/maze_bg.wasm \
		site-src/memory_match/convert_code_points.py \
		site-src/memory_match/gear.png \
		site-src/memory_match/memory_match.css \
		site-src/memory_match/memory_match.js \
		site-src/objective-c-tuesdays/arrays.html \
		site-src/objective-c-tuesdays/at-property_and_at-synthesize.html \
		site-src/objective-c-tuesdays/atomic_and_nonatomic_properties.html \
		site-src/objective-c-tuesdays/break_out_of_a_loop.html \
		site-src/objective-c-tuesdays/c_strings.html \
		site-src/objective-c-tuesdays/changing_default_property_names.html \
		site-src/objective-c-tuesdays/common_uses_for_goto.html \
		site-src/objective-c-tuesdays/concatenating_strings.html \
		site-src/objective-c-tuesdays/continue.html \
		site-src/objective-c-tuesdays/dynamic_arrays.html \
		site-src/objective-c-tuesdays/extern_and_global_variables.html \
		site-src/objective-c-tuesdays/for_loop_variations.html \
		site-src/objective-c-tuesdays/global_variables.html \
		site-src/objective-c-tuesdays/goto.html \
		site-src/objective-c-tuesdays/instance_variables.html \
		site-src/objective-c-tuesdays/instance_variables_getters_and_setters.html \
		site-src/objective-c-tuesdays/local_variables_and_function_parameters.html \
		site-src/objective-c-tuesdays/looping_in_objective-c.html \
		site-src/objective-c-tuesdays/more_about_dynamic_arrays.html \
		site-src/objective-c-tuesdays/more_nsarray_sorting.html \
		site-src/objective-c-tuesdays/regular_expressions.html \
		site-src/objective-c-tuesdays/replacing_in_strings.html \
		site-src/objective-c-tuesdays/searching_in_strings.html \
		site-src/objective-c-tuesdays/slicing_and_dicing_strings.html \
		site-src/objective-c-tuesdays/sorting_arrays.html \
		site-src/objective-c-tuesdays/static_variables.html \
		site-src/objective-c-tuesdays/static_variables_in_functions.html \
		site-src/objective-c-tuesdays/string_comparison_and_equality.html \
		site-src/objective-c-tuesdays/string_literals.html \
		site-src/objective-c-tuesdays/strings_in_objective-c.html \
		site-src/objective-c-tuesdays/synthesizing_properties.html \
		site-src/objective-c-tuesdays/the_do-while_loop.html \
		site-src/objective-c-tuesdays/the_for-in_loop.html \
		site-src/objective-c-tuesdays/the_for_loop.html \
		site-src/objective-c-tuesdays/the_while_loop.html \
		site-src/objective-c-tuesdays/unicode_string_literals.html \
		site-src/objective-c-tuesdays/variables_in_objective-c.html \
		site-src/objective-c-tuesdays/wide_character_strings.html \
		site-src/objective-c-tuesdays/writing_a_thread_safe_getter_method.html \
		site-src/random_words/make_table.py \
		site-src/random_words/random_words.css \
		site-src/random_words/random_words.js \
		site-src/random_words/words.txt \
		site-src/random_words/words.table \
		site-src/resume/resume.css \
		site-src/resume/Resume_of_Don_McCaughey.md \
		site-src/resume/Resume_of_Don_McCaughey.pdf \
		site-src/science_fiction/alastair_reynolds.page \
		site-src/science_fiction/david_weber.page \
		site-src/science_fiction/iain_m_banks.page \
		site-src/science_fiction/james_sa_corey.page \
		site-src/science_fiction/lois_mcmaster_bujold.page \
		site-src/science_fiction/neal_stephenson.page \
		site-src/science_fiction/walter_jon_williams.page \
		site-src/shell/index.page

wwwroot_files := $(shell find wwwroot -type f)


$(TMP)/checked_html.stamp.txt : \
		scripts/check-html \
		$(wwwroot_files) \
		| $$(dir $$@)
	scripts/check-html
	date > $@


$(TMP)/uploaded.stamp.txt : \
		$(TMP)/checked_html.stamp.txt \
		scripts/upload \
		$(wwwroot_files) \
		| $$(dir $$@)
	scripts/upload
	date > $@


##### gen ##########


##### maze ##########

site-src/maze/maze_bg.wasm : maze/pkg/maze_bg.wasm | $$(dir $$@)
	cp $< $@


site-src/maze/maze_bg.js : maze/pkg/maze.js | $$(dir $$@)
	cp $< $@


maze/pkg/maze_bg.wasm \
maze/pkg/maze.js : $(TMP)/maze-wasm-generated.stamp.txt
	@:


$(TMP)/maze-wasm-generated.stamp.txt : maze/Cargo.toml maze/src/lib.rs | $$(dir $$@)
	cd maze && wasm-pack build --target no-modules
	date > $@


$(TMP) \
site-src/maze :
	mkdir -p $@
