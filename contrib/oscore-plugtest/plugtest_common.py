import shutil
from pathlib import Path

# When Python 3.5 support is dropped (and PyPy has evolved beyond that
# point), .as_posix() can be dropped

import cbor

from aiocoap import oscore

contextdir = Path(__file__).parent / 'common-context'

class LoggingFilesystemSecurityContext(oscore.FilesystemSecurityContext):
    def _extract_external_aad(self, message, i_am_sender, request_partiv=None):
        result = super()._extract_external_aad(message, i_am_sender, request_partiv)
        print("Verify: External AAD: bytes.fromhex(%r), %r"%(result.hex(), cbor.loads(result)))
        return result

def get_security_context(contextname, contextcopy: Path):
    """Copy the base context (disambiguated by contextname in "ab", "cd") onto
    the path in contextcopy if it does not already exist, and load the
    resulting context with the given role. The context will be monkey-patched
    for debugging purposes."""
    if not contextcopy.exists():
        contextcopy.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree((contextdir / contextname).as_posix(), contextcopy.as_posix())

        print("Context %s copied to %s" % (contextname, contextcopy))

    return LoggingFilesystemSecurityContext(contextcopy.as_posix())

def additional_verify(description, lhs, rhs):
    if lhs == rhs:
        print("Additional verify passed: %s"%description)
    else:
        print("Additional verify failed (%s != %s): %s"%(lhs, rhs, description))
