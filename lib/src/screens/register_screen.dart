import 'package:flutter/material.dart';
import '../services/hw_id_service.dart';

class RegisterScreen extends StatefulWidget {
  const RegisterScreen({super.key});

  @override
  State<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  final HwIdService _hw = HwIdService();
  String _hwId = 'loading...';
  final TextEditingController _codeController = TextEditingController();
  String _message = '';

  @override
  void initState() {
    super.initState();
    _loadHw();
  }

  Future<void> _loadHw() async {
    try {
      final id = await _hw.getHwId();
      setState(() => _hwId = id);
    } catch (e) {
      setState(() => _hwId = 'failed to read HW ID: \$e');
    }
  }

  void _submit() {
    final code = _codeController.text;
    final ok = _hw.validate(_hwId, code);
    setState(() {
      _message = ok ? 'Aktivasi berhasil — simpan akun!' : 'Kode aktivasi tidak valid.';
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Register')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Text('HW ID (salin dan berikan ke penyedia aktivasi):'),
            SelectableText(_hwId),
            const SizedBox(height: 12),
            TextField(
              controller: _codeController,
              decoration: const InputDecoration(
                labelText: 'Kode Aktivasi',
              ),
            ),
            const SizedBox(height: 12),
            ElevatedButton(onPressed: _submit, child: const Text('Aktivasi')),
            const SizedBox(height: 12),
            Text(_message, style: const TextStyle(color: Colors.red)),
          ],
        ),
      ),
    );
  }
}
