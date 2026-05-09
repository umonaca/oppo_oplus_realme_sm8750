import os
import glob

os.chdir(r"d:\Users\Andrea-TB\Desktop\Scene隐藏\oppo_oplus_realme_sm8750")

def patch_files(pattern, search, replace):
    count = 0
    for filepath in glob.glob(pattern):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        if search in content:
            content = content.replace(search, replace)
            with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
                f.write(content)
            count += 1
    print(f"Patched {count} files for {pattern}")

yaml_append = """echo "CONFIG_KSU=y" >> ./common/arch/arm64/configs/gki_defconfig
          echo "CONFIG_BPF_LSM=y" >> ./common/arch/arm64/configs/gki_defconfig
          echo "CONFIG_BPF_TRAMPOLINE=y" >> ./common/arch/arm64/configs/gki_defconfig
          echo "CONFIG_DYNAMIC_FTRACE=y" >> ./common/arch/arm64/configs/gki_defconfig
          echo "CONFIG_DYNAMIC_FTRACE_WITH_DIRECT_CALLS=y" >> ./common/arch/arm64/configs/gki_defconfig
          echo "CONFIG_DEBUG_INFO_BTF=y" >> ./common/arch/arm64/configs/gki_defconfig"""

sh_append = """echo "CONFIG_KSU=y" >> "$DEFCONFIG_FILE"
echo "CONFIG_BPF_LSM=y" >> "$DEFCONFIG_FILE"
echo "CONFIG_BPF_TRAMPOLINE=y" >> "$DEFCONFIG_FILE"
echo "CONFIG_DYNAMIC_FTRACE=y" >> "$DEFCONFIG_FILE"
echo "CONFIG_DYNAMIC_FTRACE_WITH_DIRECT_CALLS=y" >> "$DEFCONFIG_FILE"
echo "CONFIG_DEBUG_INFO_BTF=y" >> "$DEFCONFIG_FILE" """

patch_files('.github/workflows/fastbuild_*.yml', 'echo "CONFIG_KSU=y" >> ./common/arch/arm64/configs/gki_defconfig', yaml_append)
patch_files('local/builder_*.sh', 'echo "CONFIG_KSU=y" >> "$DEFCONFIG_FILE"', sh_append)

lsm_yaml_append = """#跳过将uapi标准头安装到 usr/include 目录的不必要操作，节省编译时间
          cd ./common
          sed -i '/^config LSM$/,/^help$/{ /^[[:space:]]*default/ { /bpf/! s/selinux/bpf,selinux/ } }' security/Kconfig
          cd .."""
          
lsm_sh_append = """#跳过将uapi标准头安装到 usr/include 目录的不必要操作，节省编译时间
echo "CONFIG_HEADERS_INSTALL=n" >> "$DEFCONFIG_FILE"
cd common
sed -i '/^config LSM$/,/^help$/{ /^[[:space:]]*default/ { /bpf/! s/selinux/bpf,selinux/ } }' security/Kconfig
cd .."""

patch_files('.github/workflows/fastbuild_*.yml', '#跳过将uapi标准头安装到 usr/include 目录的不必要操作，节省编译时间', lsm_yaml_append)
patch_files('local/builder_*.sh', '#跳过将uapi标准头安装到 usr/include 目录的不必要操作，节省编译时间\necho "CONFIG_HEADERS_INSTALL=n" >> "$DEFCONFIG_FILE"', lsm_sh_append)
