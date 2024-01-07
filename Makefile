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


##### Maze ##########

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
