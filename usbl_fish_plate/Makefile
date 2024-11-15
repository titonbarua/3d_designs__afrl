PREFIX=usbl_fish_plate

F3D_COLOR=1.0,0.1,0.1
F3D_ROUGHNESS=0.3
F3D_METALLIC=0.7

F3D_CAM_POS="-270.223,-325.058,708.206"
F3D_CAM_VIEW_UP="0.533599,0.678345,0.505094"
F3D_CAM_FOCAL_POINT="-12.5642,5.16936,-7.48128"
F3D_CAM_VIEW_ANGLE="19.4333"

F3D_OPTS=--axis --grid --no-background --resolution=1600,1600


all: render_png


export_stl: ./$(PREFIX)_design.py
	python3 ./$(PREFIX)_design.py export_stl $(PREFIX)_design.stl


render_png: ./$(PREFIX)_design.stl
	f3d --color=$(F3D_COLOR) $(F3D_OPTS) \
		--roughness=$(F3D_ROUGHNESS) \
		--metallic=$(F3D_METALLIC) \
		--camera-position=$(F3D_CAM_POS) \
		--camera-focal-point=$(F3D_CAM_FOCAL_POINT) \
		--camera-view-up=$(F3D_CAM_VIEW_UP) \
		--camera-view-angle=$(F3D_CAM_VIEW_ANGLE) \
		--raytracing --denoise --anti-aliasing --ambient-occlusion --samples 10 \
		--output=./rendering.png \
	       	./$(PREFIX)_design.stl 
