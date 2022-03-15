TMP ?= $(abspath tmp)


.SECONDEXPANSION :


.PHONY : all
all : maze


.PHONY : maze
maze : \
		site-src/maze/maze_bg.wasm \
		site-src/maze/maze.js


.PHONY : clean
clean :
	rm -rf $(TMP)
	rm -rf maze/pkg


site-src/maze/maze_bg.wasm \
site-src/maze/maze.js : site-src/maze/% : maze/pkg/% | $$(dir $$@)
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

