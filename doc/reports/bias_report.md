# Đánh giá LLM Judge Phase B

Nhóm: **Latentia**. Người phụ trách: **Nguyễn Minh Thắng — 2A202602706**.
Nguồn: `artifacts/judge_results.json`; run_kind **live**, format version 2.
Timestamp: `2026-10-12T15:14:31.101132+00:00` — **12/10/2026 22:14:31 UTC+07:00**.
Generation model: `gpt-4o-mini-2024-07-18`;
judge model yêu cầu: `gpt-4o-mini`.

Đã chạy một batch mới trên bộ nguồn cuối của nhóm: 5 cặp, 10 lượt pairwise,
10 binary judgments; không dùng nhãn human/notes trong prompt và không dùng mock
làm artifact. Lượt này thay artifact cũ để báo cáo khớp chính xác bản nộp cuối.

## Năm cặp A/B và hai lượt

A từ artifacts/answers_50q.json:answer; B từ fixtures/human_labels_10q.json:model_answer;
reference từ fixtures/test_set_50q.json:ground_truth. IDs 1,5,12,21,41 giữ nguyên.
Winner và scores lượt hai trong bảng đã quy đổi về A/B gốc. Reasoning nguyên văn
lượt hai vẫn dùng tên A/B theo thứ tự đã swap; không đọc nó như thứ tự lượt một.

| ID | A gốc | B gốc | Pass 1 | Pass 2 đã quy đổi | Final | Nhất quán | Scores 1 A/B | Scores 2 A/B |
|---|---|---|---|---|---|---|---|---|
| 1 | Không tìm thấy. | Nhân viên được nghỉ 3 ngày làm việc có lương khi kết hôn. | B | B | B | True | 0/1 | 0/1 |
| 5 | Cần phê duyệt của Giám đốc điều hành (CEO). | Cần Giám đốc phòng ban phê duyệt. | A | A | A | True | 1/0 | 1/0 |
| 12 | Thưởng Tết tối thiểu cho nhân viên chính thức có từ 6 tháng trở lên là **1 tháng lương**. | Nhân viên được thưởng Tết tối thiểu 1 tháng lương. | A | tie | tie | False | 1/0.8 | 1/1 |
| 21 | Không tìm thấy. | Được nghỉ 18 ngày phép (15 cơ bản + 3 thâm niên). Lương Senior từ 20 đến 35 triệu. | B | B | B | True | 0/1 | 0/1 |
| 41 | Không tìm thấy. | Nhân viên được nghỉ 12 ngày phép năm. | B | A | tie | False | 0/0.5 | 1/0 |

### ID 1 — Nhân viên được nghỉ bao nhiêu ngày khi kết hôn?

- Lượt 1: Answer B provides the correct information as per the reference, stating that employees are entitled to 3 days of paid leave when getting married. Answer A does not provide any relevant information and is therefore incomplete.
- Lượt 2 (B gốc hiển thị trước, A gốc sau): Answer A accurately reflects the information provided in the reference, stating that employees are entitled to 3 days of paid leave for marriage. Answer B, on the other hand, does not provide any relevant information and simply states that no information was found, making it incomplete.

### ID 5 — Muốn mua thiết bị trị giá 55 triệu cần ai phê duyệt?

- Lượt 1: Answer A correctly identifies that the approval of the CEO is required for purchases over 50 million VND, aligning with the reference. Answer B incorrectly states that the department head's approval is sufficient, which does not meet the criteria outlined in the reference.
- Lượt 2 (B gốc hiển thị trước, A gốc sau): Answer B correctly identifies that the approval of the CEO is required for purchases over 50 million VND, as stated in the reference. Answer A incorrectly states that the department director's approval is sufficient, which does not align with the policy reference.

### ID 12 — Thưởng Tết tối thiểu cho nhân viên chính thức có từ 6 tháng trở lên là bao nhiêu?

- Lượt 1: Answer A provides a complete and accurate response to the question, explicitly stating that the minimum Tết bonus for employees with 6 months or more of service is 1 month of salary. Answer B, while correct, is less specific and does not directly address the condition of having 6 months of service, making it less complete.
- Lượt 2 (B gốc hiển thị trước, A gốc sau): Both answers accurately convey the minimum Tết bonus for employees with 6 months or more of service as 1 month of salary. They are both complete and concise, providing the same essential information without unnecessary details.

### ID 21 — Một nhân viên Senior có 9 năm thâm niên được nghỉ bao nhiêu ngày phép năm và lương trong khoảng nào?

- Lượt 1: Answer B provides a complete and accurate response to the question, detailing both the number of vacation days and the salary range for a Senior employee with 9 years of experience. Answer A, on the other hand, does not provide any relevant information and simply states 'Không tìm thấy' (Not found), making it unhelpful.
- Lượt 2 (B gốc hiển thị trước, A gốc sau): Answer A provides a complete and accurate response to the question regarding the number of vacation days and salary range for a Senior employee with 9 years of experience, directly referencing the policy. Answer B, on the other hand, does not provide any relevant information and simply states that it cannot be found.

### ID 41 — Nhân viên được nghỉ bao nhiêu ngày phép năm?

- Lượt 1: Answer B provides a specific number of leave days (12 days), which is relevant to the question. However, it is based on the outdated policy from 2023. Answer A states 'Không tìm thấy' (Not found), which does not provide any useful information. While both answers are incomplete, Answer B at least offers a concrete figure, even if it is not the most current one. Therefore, B is the better choice despite its inaccuracies.
- Lượt 2 (B gốc hiển thị trước, A gốc sau): Answer A incorrectly states that employees are entitled to 12 days of leave, which is based on the outdated policy from 2023. Answer B, while not providing a specific answer, correctly indicates that there is no information found, which aligns with the need to prioritize the current policy from 2024. Therefore, Answer B is more accurate in the context of the question.

## Position inconsistency và verbosity proxy

Position inconsistency: **2/5 = 40%**, IDs **12 và 41**.
Longer-answer win rate: **3/3 = 100%** trên decisive cases IDs **1,5,21**;
A thắng và dài hơn 1 lần, B thắng và dài hơn 2 lần. Tie không vào mẫu số verbosity.

ID 12 chuyển từ A sang tie: A nêu rõ điều kiện chính thức/ít nhất 6 tháng,
B ngắn hơn; judge chưa ổn định khi đánh giá thông tin ngầm từ câu hỏi.
ID 41 chuyển B sang A: B dùng 12 ngày của chính sách cũ, trong khi reference
hiện hành là **15 ngày**; A abstain. Lượt một ưu tiên có số dù cũ, lượt hai
ưu tiên abstention hơn câu sai. Consensus tie cho thấy winner tương đối không
thể dùng làm label tốt/xấu của một answer.

Tỷ lệ dài hơn thắng 100% chưa chứng minh độ dài là nguyên nhân: ở các cặp decisive,
winner đồng thời đúng/đủ hơn (3 ngày nghỉ kết hôn, đúng cấp CEO, đầy đủ phép/lương).
Cần cặp cùng chất lượng chỉ thay lượng từ dư thừa và sample holdout lớn hơn.
40% bất nhất trên 5 cặp là tín hiệu điều tra, không là xác suất bias production.

## Calibration đúng model_answer

Helper chỉ nhận question, model_answer gốc và reference. Nhãn human/notes chỉ
được đối chiếu sau judge, không gửi vào prompt; không thay bằng answer pipeline.

| ID | Model answer gốc | Judge | Human | Agree | Reasoning |
|---|---|---|---|---|---|
| 1 | Nhân viên được nghỉ 3 ngày làm việc có lương khi kết hôn. | 1 | 1 | True | Câu trả lời chính xác theo thông tin trong reference, nêu rõ số ngày nghỉ và điều kiện không trừ vào phép năm. |
| 5 | Cần Giám đốc phòng ban phê duyệt. | 0 | 0 | True | Câu trả lời sai vì cần Tổng Giám đốc phê duyệt chứ không phải Giám đốc phòng ban. |
| 12 | Nhân viên được thưởng Tết tối thiểu 1 tháng lương. | 1 | 1 | True | Câu trả lời chính xác theo thông tin trong reference, nêu rõ điều kiện và mức thưởng cho nhân viên chính thức có từ 6 tháng trở lên. |
| 21 | Được nghỉ 18 ngày phép (15 cơ bản + 3 thâm niên). Lương Senior từ 20 đến 35 triệu. | 1 | 1 | True | Câu trả lời chính xác theo reference, nêu rõ số ngày phép và khoảng lương cho nhân viên Senior với 9 năm thâm niên. |
| 23 | Hoàn trả 25 triệu vì chưa đủ 1 năm cam kết. | 1 | 1 | True | Câu trả lời chính xác theo thông tin trong reference, nêu rõ lý do hoàn trả 25 triệu do chưa đủ 1 năm cam kết. |
| 29 | Trưởng phòng phê duyệt. Phạt 2% tháng trên 8 triệu. | 0 | 0 | True | Câu trả lời thiếu thông tin về sự cần thiết có sự phê duyệt của Kế toán trưởng bên cạnh Trưởng phòng. Ngoài ra, phí phạt được tính cho quá hạn 15 ngày, không phải là 2% trên tổng số tiền tạm ứng. |
| 33 | Phép: 19 ngày. Phụ cấp: 1.500.000 VNĐ/tháng. | 1 | 1 | True | Câu trả lời cung cấp đúng số ngày phép và tổng phụ cấp hàng tháng theo thông tin trong tài liệu tham khảo. |
| 41 | Nhân viên được nghỉ 12 ngày phép năm. | 0 | 0 | True | Câu trả lời sai vì nó dựa trên chính sách cũ (v2023) thay vì chính sách hiện hành (v2024) là 15 ngày phép năm. |
| 46 | Nhân viên thử việc không được nghỉ phép năm và phải xin nghỉ không lương nếu cần. | 1 | 1 | True | Câu trả lời chính xác theo reference, nêu rõ rằng nhân viên thử việc không được nghỉ phép năm và phải xin nghỉ không lương nếu cần, đồng thời không bỏ qua điều kiện cần có sự phê duyệt của trưởng phòng. |
| 50 | Được, miễn là đảm bảo kết nối an toàn. | 0 | 0 | True | Câu trả lời sai vì cho phép sử dụng VPN cá nhân trong khi chính sách rõ ràng cấm điều này. |

Agreement **10/10**; judge/human đều có 6 nhãn 1 và 4 nhãn 0:
`p_o=1`, `p_e=0.6×0.6+0.4×0.4=0.52`,
`κ=(1−0.52)/(1−0.52)=1.0`. Lần này đạt ngưỡng bonus κ>0.6.
Agreement không bảo đảm mọi reasoning faithful: ở một số câu judge suy thêm
điều kiện từ reference rồi gán cho candidate. Phải audit explanation riêng,
không xem nhãn đúng là bằng chứng giải thích hoàn toàn đúng.

## Kiểm chứng và giới hạn

Artifact qua schema, ids, nguồn dữ liệu, phép tính và source hashes.
Kiểm tra cuối `python scripts/check_lab.py --with-tests`: **131 tests pass**,
3 live integration tests deselected, **0 failed checks**. Không chạy lại A/C
vì nhóm đã cung cấp artifacts và tránh lặp chi phí không cần thiết.

Source JSON giữ đúng bytes CRLF của các lượt gốc bằng .gitattributes; không sửa
labels, metric values hoặc expected hashes để vượt checker. Chỉ thêm batch B thật
và cập nhật báo cáo tương ứng. Pairwise dùng temperature=0, JSON mode, reference
rubric accuracy/completeness/conciseness; temperature=0 không đảm bảo mọi lần giống hệt.
Candidate/reference được đóng gói là dữ liệu không đáng tin, không phải instructions.

Mẫu chỉ 5 cặp/10 nhãn, chưa đo stress prompt injection hoặc tổng quát sang dữ liệu mới.
Dùng swap consensus và human review cho case bất nhất/phiên bản/phủ định;
không dùng LLM judge như chân lý tuyệt đối. SDK mock chỉ dùng kiểm tra logic/contracts.

## Source hashes và nguồn hỗ trợ

- `answers_50q.json`: `0cc95f5a347464fb81ccff2005e7078498c9e059d6272cc5e970d3420372067e`.
- `test_set_50q.json`: `0e87f26e020a32c62ea0864940720618f39600b9d3378193704cf2f86e88446d`.
- `human_labels_10q.json`: `e72338bd99c3d0165348c11997735bbb87c978fe018c24dfd29c9801d5c2b2c1`.

Nguồn: README, ASSIGNMENT, RUBRIC, REPORT_SCHEMAS và scaffold. Codex hỗ trợ
implementation, kiểm thử và phân tích JSON thật; tên người phụ trách là
Nguyễn Minh Thắng, MSSV 2A202602706. Không có API key trong báo cáo/commit.
