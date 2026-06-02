"""RSA SHA256 signing helpers for Antom API messages.

Antom APIs use RSA SHA256 signatures in request/response headers. The exact
canonical string can vary by product/version, so all canonicalization is kept in
this module to make production adjustments localized after live-doc validation.
"""

from __future__ import annotations

import base64
from dataclasses import dataclass

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


@dataclass(frozen=True)
class SignatureParts:
    algorithm: str
    key_version: str
    signature: str


def _normalize_pem(value: str) -> bytes:
    return (value or "").replace("\\n", "\n").encode("utf-8")


def load_private_key(private_key_pem: str):
    """Load an RSA private key from a PEM string provided via environment."""
    return serialization.load_pem_private_key(_normalize_pem(private_key_pem), password=None)


def load_public_key(public_key_pem: str):
    """Load an RSA public key from a PEM string provided via environment."""
    return serialization.load_pem_public_key(_normalize_pem(public_key_pem))


def build_signature_content(method: str, uri_path: str, client_id: str, request_time: str, body: str) -> bytes:
    """Build canonical content for signing.

    TODO: verify canonical string format against the exact Antom product docs
    before production go-live. Antom public docs describe RSA256 signatures with
    request path, client id, request time and JSON body in signed content.
    """
    canonical = f"{method.upper()} {uri_path}\n{client_id}.{request_time}.{body}"
    return canonical.encode("utf-8")


def sign_request(private_key_pem: str, method: str, uri_path: str, client_id: str, request_time: str, body: str) -> str:
    """Return a base64 RSA-SHA256 signature for an Antom API request."""
    private_key = load_private_key(private_key_pem)
    signature = private_key.sign(
        build_signature_content(method, uri_path, client_id, request_time, body),
        padding.PKCS1v15(),
        hashes.SHA256(),
    )
    return base64.b64encode(signature).decode("ascii")


def parse_signature_header(value: str) -> SignatureParts:
    """Parse Antom-style Signature header into parts."""
    parts = {}
    for item in (value or "").split(","):
        if "=" not in item:
            continue
        key, raw_value = item.strip().split("=", 1)
        parts[key] = raw_value.strip().strip('"')
    return SignatureParts(
        algorithm=parts.get("algorithm", ""),
        key_version=parts.get("keyVersion", ""),
        signature=parts.get("signature", ""),
    )


def verify_signature(public_key_pem: str, signature: str, method: str, uri_path: str, client_id: str, request_time: str, body: str) -> bool:
    """Verify a base64 RSA-SHA256 signature."""
    if not signature:
        return False
    public_key = load_public_key(public_key_pem)
    try:
        public_key.verify(
            base64.b64decode(signature),
            build_signature_content(method, uri_path, client_id, request_time, body),
            padding.PKCS1v15(),
            hashes.SHA256(),
        )
    except (InvalidSignature, ValueError):
        return False
    return True
