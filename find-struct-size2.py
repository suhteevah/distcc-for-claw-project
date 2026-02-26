import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("10.0.0.6", username="root", password="cnc-server-2024!", timeout=15)

def run(cmd, timeout=120):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    return out + err

# Approach 1: Try to install bpftool (without reboot if possible)
print("=== 1. Try zypper for bpftool ===")
print(run(r"""
# Check if bpftool is in any package
zypper -n search bpftool 2>&1 | head -10
# Try direct install (non-transactional, might work for tools)
zypper -n install --no-recommends bpftool 2>&1 | tail -10
""", timeout=120))

# Approach 2: Try to build bpftool from kernel source
print("\n=== 2. Check for bpftool in kernel source ===")
print(run(r"ls /root/wifi-build/linux-6.12/tools/bpf/bpftool/ 2>/dev/null | head -5"))

# Approach 3: Parse BTF binary directly with Python
print("\n=== 3. Parse BTF with Python ===")
run(r"""cat > /tmp/parse_btf.py << 'PYEOF'
import struct
import sys

# Read the BTF data
with open('/sys/kernel/btf/vmlinux', 'rb') as f:
    data = f.read()

# BTF header format
MAGIC = 0xEB9F
HDR_SIZE = 24

magic, version, flags, hdr_len = struct.unpack_from('<HBBI', data, 0)
type_off, type_len, str_off, str_len = struct.unpack_from('<IIII', data, 8)

if magic != MAGIC:
    print(f"Bad magic: {magic:#x}")
    sys.exit(1)

print(f"BTF: version={version}, hdr_len={hdr_len}")
print(f"  types: off={type_off}, len={type_len}")
print(f"  strings: off={str_off}, len={str_len}")

str_base = hdr_len + str_off
type_base = hdr_len + type_off

# Get string from string table
def get_string(off):
    if off == 0:
        return ""
    start = str_base + off
    end = data.index(b'\0', start)
    return data[start:end].decode('utf-8', errors='replace')

# Parse types to find usb_host_endpoint
# BTF type kinds
BTF_KIND_STRUCT = 4
BTF_KIND_INT = 1
BTF_KIND_PTR = 2
BTF_KIND_ARRAY = 3
BTF_KIND_UNION = 5
BTF_KIND_ENUM = 6
BTF_KIND_FWD = 7
BTF_KIND_TYPEDEF = 8
BTF_KIND_VOLATILE = 9
BTF_KIND_CONST = 10
BTF_KIND_RESTRICT = 11

pos = type_base
type_id = 1
target_id = None
target_name = "usb_host_endpoint"
target2_name = "usb_host_interface"

types = {}  # id -> info

while pos < type_base + type_len:
    name_off, info, size_or_type = struct.unpack_from('<III', data, pos)
    pos += 12

    kind = (info >> 24) & 0x1f
    vlen = info & 0xffff
    kflag = (info >> 31) & 1

    name = get_string(name_off)

    types[type_id] = {'name': name, 'kind': kind, 'size': size_or_type, 'vlen': vlen}

    if kind == BTF_KIND_STRUCT or kind == BTF_KIND_UNION:
        members = []
        for i in range(vlen):
            m_name_off, m_type, m_offset = struct.unpack_from('<III', data, pos)
            pos += 12
            if kflag:
                m_bitfield_size = m_offset >> 24
                m_bit_offset = m_offset & 0xffffff
            else:
                m_bitfield_size = 0
                m_bit_offset = m_offset
            members.append({
                'name': get_string(m_name_off),
                'type': m_type,
                'bit_offset': m_bit_offset,
                'bitfield_size': m_bitfield_size
            })
        types[type_id]['members'] = members

        if name == target_name:
            print(f"\nFound '{target_name}' at type_id={type_id}, sizeof={size_or_type}")
            for m in members:
                print(f"  +{m['bit_offset']//8:3d} ({m['bit_offset']:4d} bits): {m['name']} (type_id={m['type']})")
            target_id = type_id

        if name == target2_name:
            print(f"\nFound '{target2_name}' at type_id={type_id}, sizeof={size_or_type}")
            for m in members:
                print(f"  +{m['bit_offset']//8:3d} ({m['bit_offset']:4d} bits): {m['name']} (type_id={m['type']})")

        if name == "usb_endpoint_descriptor":
            print(f"\nFound 'usb_endpoint_descriptor' at type_id={type_id}, sizeof={size_or_type}")

        if name == "usb_ss_ep_comp_descriptor":
            print(f"\nFound 'usb_ss_ep_comp_descriptor' at type_id={type_id}, sizeof={size_or_type}")

        if name == "usb_ssp_isoc_ep_comp_descriptor":
            print(f"\nFound 'usb_ssp_isoc_ep_comp_descriptor' at type_id={type_id}, sizeof={size_or_type}")

    elif kind == BTF_KIND_ARRAY:
        # Read array info
        arr_type, idx_type, nelems = struct.unpack_from('<III', data, pos)
        pos += 12

    elif kind == BTF_KIND_ENUM:
        for i in range(vlen):
            pos += 8  # name_off + val

    elif kind == 19:  # BTF_KIND_ENUM64
        for i in range(vlen):
            pos += 12

    elif kind == BTF_KIND_FWD:
        pass

    elif kind == BTF_KIND_TYPEDEF:
        pass

    elif kind == BTF_KIND_VOLATILE or kind == BTF_KIND_CONST or kind == BTF_KIND_RESTRICT:
        pass

    elif kind == BTF_KIND_INT:
        pos += 4  # encoding

    elif kind == BTF_KIND_PTR:
        pass

    elif kind == 12:  # BTF_KIND_FUNC
        pass

    elif kind == 13:  # BTF_KIND_FUNC_PROTO
        for i in range(vlen):
            pos += 8  # name_off + type

    elif kind == 14:  # BTF_KIND_VAR
        pos += 4

    elif kind == 15:  # BTF_KIND_DATASEC
        for i in range(vlen):
            pos += 12

    elif kind == 16:  # BTF_KIND_FLOAT
        pass

    elif kind == 17:  # BTF_KIND_DECL_TAG
        pos += 4

    elif kind == 18:  # BTF_KIND_TYPE_TAG
        pass

    else:
        # Unknown kind, skip
        pass

    type_id += 1

PYEOF
""")

print(run("python3 /tmp/parse_btf.py", timeout=60))

client.close()
print("\n=== DONE ===")
