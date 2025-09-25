import 'dart:convert';
import 'package:crypto/crypto.dart';
import 'package:device_info_plus/device_info_plus.dart';

/// Service to produce a human-visible HW ID and to generate activation code
class HwIdService {
  final DeviceInfoPlugin _deviceInfo = DeviceInfoPlugin();

  /// Returns a readable HW ID string composed from device identifiers.
  Future<String> getHwId() async {
    final androidInfo = await _deviceInfo.androidInfo;
    final base = '${androidInfo.id ?? ''}|${androidInfo.model}|${androidInfo.manufacturer}';
    return base;
  }

  /// Generates activation code from HW ID using SHA-256, then taking
  /// first 2 chars and last 4 chars of the hex digest (uppercase).
  String generateActivationCode(String hwId) {
    final bytes = utf8.encode(hwId);
    final digest = sha256.convert(bytes).toString();
    final partA = digest.substring(0, 2);
    final partB = digest.substring(digest.length - 4);
    return (partA + partB).toUpperCase();
  }

  /// Validates given code against HW ID
  bool validate(String hwId, String inputCode) {
    return generateActivationCode(hwId) == inputCode.trim().toUpperCase();
  }
}
