# Split model weights — `ViT-B-32.pt`

The OpenAI CLIP `ViT-B/32` checkpoint (354 MB) is split here into 20 parts
(`ViT-B-32.pt.part00` … `part19`, ~17.7 MB each) so it can be transferred through
channels with file-size limits (e.g. GitHub's 100 MB per-file cap). Reassembling
them reproduces the **exact** original file (verified byte-for-byte).

Expected SHA-256 of the rebuilt file:
`40d365715913c9da98579312b702a82c18be219cc2a73407c4526f58eba950af`

## Rebuild (recommended — cross-platform, auto-verifies)

From inside this `model_parts/` directory:

```bash
python rebuild.py
```

This writes `../ViT-B-32.pt` and checks its SHA-256. A final `OK:` line means it
matches the official checkpoint. Then point the classifier at it:

```python
clip_classify(..., model_name="ViT-B-32.pt")   # or the absolute path
```

## Manual rebuild (fallback, no Python)

**Linux / macOS / WSL:**
```bash
cat ViT-B-32.pt.part?? > ViT-B-32.pt
sha256sum -c original.sha256        # should print: ViT-B-32.pt: OK
```

**Windows (cmd):**
```bat
copy /b ViT-B-32.pt.part00+ViT-B-32.pt.part01+ViT-B-32.pt.part02+ViT-B-32.pt.part03+ViT-B-32.pt.part04+ViT-B-32.pt.part05+ViT-B-32.pt.part06+ViT-B-32.pt.part07+ViT-B-32.pt.part08+ViT-B-32.pt.part09+ViT-B-32.pt.part10+ViT-B-32.pt.part11+ViT-B-32.pt.part12+ViT-B-32.pt.part13+ViT-B-32.pt.part14+ViT-B-32.pt.part15+ViT-B-32.pt.part16+ViT-B-32.pt.part17+ViT-B-32.pt.part18+ViT-B-32.pt.part19 ViT-B-32.pt
certutil -hashfile ViT-B-32.pt SHA256
```

**Windows (PowerShell):**
```powershell
$out = [System.IO.File]::Create("ViT-B-32.pt")
Get-ChildItem ViT-B-32.pt.part?? | Sort-Object Name | ForEach-Object {
    $bytes = [System.IO.File]::ReadAllBytes($_.FullName); $out.Write($bytes, 0, $bytes.Length)
}
$out.Close()
(Get-FileHash ViT-B-32.pt -Algorithm SHA256).Hash
```

For the manual routes, confirm the printed hash equals the expected value above.
If it doesn't, a part is missing, corrupt, or concatenated out of order — don't use it.

## Files here

- `ViT-B-32.pt.part00` … `part19` — the split pieces
- `rebuild.py` — reassemble + verify (stdlib only)
- `parts.sha256` — per-part checksums (`sha256sum -c parts.sha256` to check the pieces)
- `original.sha256` — checksum of the reassembled whole file
