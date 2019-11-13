
r"""
harvest
copy all from Wix/Fragment/DirectoryRef/Directory
paste to Wix/Product/<DirectoryRef Id="application_root_directory">
for each component:
	if .exe:
		change component id to "main_exe_component"
	get component id
	change Source from "SourceDir\*" to "SourceDir\Goblin Care\*"

paste component ids to Wix/Product/Feature/ComponentRef/Id
generate new guid for product id and UpgradeCode
bump minor version
"""
