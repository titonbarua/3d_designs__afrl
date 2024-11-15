PREFIX=usbl_fish_transducer_holder

F3D_COLOR=0.4,0.2,0.7
F3D_ROUGHNESS=0.7
F3D_METALLIC=0.3

F3D_CAM_POS="260.125,-129.528,232.701"
F3D_CAM_VIEW_UP="-0.559081,0.269519,0.784084"
F3D_CAM_FOCAL_POINT="5.64427,-6.84427,11.1518"
F3D_CAM_VIEW_ANGLE="23.9444"

F3D_OPTS=--axis --grid --no-background --resolution=1600,1600

DESIGN_FILE=$(PREFIX).py
STL_FILE=$(PREFIX).stl


all: render_png


export_stl: $(DESIGN_FILE)
	python3 $(DESIGN_FILE) export_stl $(STL_FILE)


render_png: export_stl
	f3d --color=$(F3D_COLOR) $(F3D_OPTS) \
		--roughness=$(F3D_ROUGHNESS) \
		--metallic=$(F3D_METALLIC) \
		--camera-position=$(F3D_CAM_POS) \
		--camera-focal-point=$(F3D_CAM_FOCAL_POINT) \
		--camera-view-up=$(F3D_CAM_VIEW_UP) \
		--camera-view-angle=$(F3D_CAM_VIEW_ANGLE) \
		--raytracing --denoise --anti-aliasing --ambient-occlusion --samples 10 \
		--output=./rendering.png \
	       	./$(STL_FILE)
